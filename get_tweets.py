# for further information consult http://docs.tweepy.org/en/v3.8.0/getting_started.html

import os
import sys
import tweepy as tw
import codecs
import csv
import pandas

# sys.stdout = open('log.txt', 'w')
# sys.stdout.reconfigure(encoding='utf-8')
# print(sys.stdout.encoding)
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
consumer_key = 'xdwGUUvltBap445IS4frt2zAx'
consumer_secret = 'ikT4cgvsDiZ0Y9ugGm3sPBW6l05D5V9liVQCSZXRMm4jMZN63f'
access_token = '1235246504140406784-giaxeTnxS0oLzkO64R4n9sRwAIOdMD'
access_secret = 'Wx3qNuWa8o2TMECjQn5qZArT4tclcyaiqIYeUQXsBT1GL'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# query = "$TSLA"
stock_query = "$AAPL"
company_query = "apple"

# query is NOT case-sensitive
# removed since=date_since
# decided to go for extended tweet mode without the retweets for better sentiment analysis 
# CORONA SCORE: COVID, virus, corona
tweets = tw.Cursor(api.search, tweet_mode="extended", q="zoom -filter:retweets", lang="en", since="2020-03-28", until="2020-03-29").items(10000)

# tweet.created_at is in UTC 
with open("file.csv", mode="w", encoding="utf-8") as file: 
	file_writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for count, tweet in enumerate(tweets): 
		file_writer.writerow([count, tweet.full_text, tweet.retweet_count, tweet.favorite_count, tweet.created_at])

# for count, tweet in enumerate(tweets): 
# 	print("Index ", count)
# 	print(tweet.text)
# 	print(tweet.retweet_count)
# 	print(tweet.favorite_count)