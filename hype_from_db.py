# Run the following in terminal 
# cloud_sql_proxy.exe -instances=strategic-goods-273618:us-east1:hypefyn=tcp:3306

import pymysql, argparse
import pandas as pd
import numpy as np
import tokenizer
from hype_score import hype_scores
import pickle


def get_sentiment(model, text):

    # Tokenize the text of the tweet
    tokens = tokenizer.tokenize([text])
    # Remove the noise
    tokens = tokenizer.remove_noise(tokens)
    # Re-merge the tweets
    text_clean = tokenizer.join_tokens(tokens)

    # Predict the sentiment
    sentiment = model.predict(text_clean)
    if sentiment[0]==4:
        sentiment = "Pos"
    elif sentiment[0]==0:
        sentiment = "Neg"
    else:
        sentiment = "Neut"
    
    return sentiment

def get_tweet_from_sql(cursor, model, grouping, company):
    
    keywords = grouping[company]    

    for key in keywords:
        cursor.execute("select count(*) from " + key + ";")
        length = cursor.fetchone()[0]
        query = "select * from " + key + ";"
        cursor.execute(query)
        tweets = {}
        for i in range(length):
            # Fetch tweet
            row = cursor.fetchone()
            tweet = {
                'keyword': company,
                'text': row[1],
                'retweets': row[2],
                'favourites': row[3],
                'timestamp': row[4].date()
            }

            # Get sentiment
            tweet['prediction'] = get_sentiment(model,tweet['text'])

            # Append to dict
            tweets[i] = tweet

            if (i+1)%1000==0:
                print(f"\t{i+1} tweets predicted from {key}")

    return pd.DataFrame.from_dict(tweets,orient='index')

def get_hype_score(tweets_sent_comp, weights=(1,1,1)):
    
    tweets_group = tweets_sent_comp.copy()
    group = tweets_sent_comp.keyword[0]
    hype_comp = {}
    i = 0

    while tweets_group.shape[0] != 0:
        time_start = tweets_group.timestamp.min()
        tw = tweets_group[tweets_group.timestamp <= time_start]# + time_delta]
        pos_hype, neg_hype = hype_scores(tw, weights)
        tweets_group.drop(tw.index,inplace=True)
        v = pos_hype - neg_hype
        hype = np.log2(v) if v > 0 else -np.log2(-v)

        hype_comp[str(time_start)] = [group,
                                        hype]
        i += 1
    
    return pd.DataFrame.from_dict(hype_comp,orient='index',columns=["keyword",group+"_hype"])


def combine_hype(hypes,companies):
    
    combined = pd.DataFrame()

    for i, comp in enumerate(companies):
        combined = pd.concat([combined, hypes[i][comp+"_hype"]],axis=1)

    combined.index.rename('datetime',inplace=True)

    return combined

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', type=str)
    parser.add_argument('--psw', type=str)
    args = parser.parse_args()

    if args.user == None or args.psw == None:
        raise Exception("user and password missing")

    connection = pymysql.connect(host='127.0.0.1',
                                user=args.user,
                                password=args.psw,
                                db='Hypefyn')
    print("Connected to Google Database")

    companies = {
        'amazon': ['amazon','amzn'],
        'corona': ['corona','covid'],
        'delta': ['delta','dal'],
        'google': ['google','goog'],
        'netflix': ['netflix','nflx'],
        'novartis': ['novartis','nvs'],
        'pfizer': ['pfizer','pfe'],
        'tesla': ['tesla','tsla'],
        'tripadvisor': ['tripadvisor','trip'],
        'uber': ['uber','uberticker'],
        'zoom': ['zoom','zm']
    }

    cursor = connection.cursor()

    with open(".models/NB_trained.pickle","rb") as file:
        sentiment_model = pickle.load(file)
        print("Pretrained model loaded")
    
    hypes = []

    for company in companies:
        tweets_sent_comp = get_tweet_from_sql(cursor,sentiment_model,companies,company)
        print(f"Predictions made for {company}")
        hypes.append(get_hype_score(tweets_sent_comp))
        print(f"Hype score computed for {company}")

    final_hype = combine_hype(hypes,companies)
    print("Final hype merged")

    final_hype.to_csv("data/tweets_hype_all.csv",header=True,index=True)

    return final_hype


if __name__ == "__main__":
    main()