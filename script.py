# for further information consult http://docs.tweepy.org/en/v3.8.0/getting_started.html

import os
import sys
import tweepy as tw
import codecs

sys.stdout = open('log.txt', 'w')
sys.stdout.reconfigure(encoding='utf-8')
# print(sys.stdout.encoding)
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
consumer_key = 'xdwGUUvltBap445IS4frt2zAx'
consumer_secret = 'ikT4cgvsDiZ0Y9ugGm3sPBW6l05D5V9liVQCSZXRMm4jMZN63f'
access_token = '1235246504140406784-giaxeTnxS0oLzkO64R4n9sRwAIOdMD'
access_secret = 'Wx3qNuWa8o2TMECjQn5qZArT4tclcyaiqIYeUQXsBT1GL'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

query = "GE"
date_since = "2020-03-01"

tweets = tw.Cursor(api.search, q=query, lang="en", since=date_since).items(1000)
for tweet in tweets: 
	print(tweet.text)