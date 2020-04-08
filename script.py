# for further information consult http://docs.tweepy.org/en/v3.8.0/getting_started.html

import os
import sys
import tweepy as tw
import codecs
import csv
import multiprocessing
# import pandas

# API Key
consumer_key = 'rWledXPWVcQCBt0Bimh0idQip'
consumer_secret = 'w1CWDEGK1hjn5KgabzbGSoTAOjffERKDjcOnHFUgQteRgTMbnY'
access_token = '1165307470325010433-7oCZroRQfVp5ch4ZErWE04PS9s0QkX'
access_secret = 'QjXkLefubpB12Kc5lbXNMLgg52lTpagasFfP8v2Da4bsF'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# query = "$TSLA"
stock_query = "$AAPL"
company_query = "apple"


def main():
    tweets = tw.Cursor(api.search, tweet_mode="extended", q="zoom -filter:retweets",
                       lang="en", since="2020-04-07", until="2020-04-08").items(100)

    with open("file.csv", mode="w", encoding="utf-8") as file:

        file_writer = csv.writer(
            file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # for count, tweet in enumerate(tweets):
        #     file_writer.writerow(
        #         [count, tweet.full_text, tweet.retweet_count, tweet.favorite_count, tweet.created_at])

        processes = []
        for count, tweet in enumerate(tweets):
            p = multiprocessing.Process(target=file_writer.writerow, args=(
                [count, tweet.full_text, tweet.retweet_count, tweet.favorite_count, tweet.created_at],))
            p.start()
            processes.append(p)

        for process in processes:
            process.join()


# query is NOT case-sensitive
# removed since=date_since
# decided to go for extended tweet mode without the retweets for better sentiment analysis
# CORONA SCORE: COVID, virus, corona
if __name__ == '__main__':
    main()
