# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%
tweets = pd.read_csv("data/tweets_pred.csv")
tweets = tweets.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
tweets.timestamp = pd.to_datetime(tweets.timestamp)

# %%

def hype_scores(tweets_group, weights=(1,1,1)):
    """
    weights = (fav,ret,vol)
    
    returns pos_hype, neg_hype
    """

    pos = tweets_group[tweets_group.Prediction == "Pos"].copy()
    neg = tweets_group[tweets_group.Prediction == "Neg"].copy()

    scores = []

    for sent in (pos, neg):
        fav = sent.favourites.sum()
        ret = sent.retweets.sum()
        vol = sent.shape[0]
        hype = weights[0]*fav + weights[1]*ret + weights[2]*vol
        scores.append(hype)

    return scores[0], scores[1]

def get_hype(df, weights=(1,1,1), delta_t=1):

    time_delta = pd.Timedelta(minutes=delta_t)
    hype = {}
    i = 0

    for key in df.keyword.unique():
        if key not in ["corona","COVID"]:
            tweets_at_key = tweets[tweets.keyword == key].copy()
            while tweets_at_key.shape[0] != 0:
                time_start = tweets_at_key.timestamp.min()
                tw = tweets_at_key[tweets_at_key.timestamp <= time_start + time_delta]
                pos_hype, neg_hype = hype_scores(tw, weights)
                tweets_at_key.drop(tw.index,inplace=True)
                hype[i] = [key,str(time_start + time_delta/2),pos_hype,neg_hype]
                i += 1
    
    return pd.DataFrame.from_dict(hype,orient='index',columns=["keyword","timestamp","pos_hype","neg_hype"])


def get_hype_corona(df, weights=(1,1,1), delta_t=1):
    
    corona_df = df[(df.keyword == "corona") | (df.keyword == "COVID")].copy()
    time_delta = pd.Timedelta(minutes=delta_t)
    hype = {}
    i = 0
    
    while corona_df.shape[0] != 0:
        time_start = corona_df.timestamp.min()
        tw = corona_df[corona_df.timestamp <= time_start + time_delta]
        pos_hype, neg_hype = hype_scores(tw, weights)
        corona_df.drop(tw.index,inplace=True)
        hype[i] = ["Coronavirus",str(time_start + time_delta/2),pos_hype,neg_hype]
        i += 1
    
    return pd.DataFrame.from_dict(hype,orient='index',columns=["keyword","timestamp","pos_hype","neg_hype"])

# %%

hype_companies = get_hype(tweets)
hype_corona = get_hype_corona(tweets)

df_to_csv = pd.concat([hype_companies, hype_corona])

df_to_csv.to_csv("data/tweets_hype.csv",header=True,index=False)

