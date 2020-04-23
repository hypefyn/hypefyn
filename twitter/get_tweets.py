import tweepy as tw
import pymysql

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
user=''
psw=''


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

tweets = tw.Cursor(api.search, tweet_mode="extended", q="$trip -filter:retweets",
                   lang="en", since="2020-04-19", until="2020-04-20").items(1000) 


connection = pymysql.connect(
    host="34.74.21.31", user=user, password=psw, db="Hypefyn", charset='utf8mb4', use_unicode=True)
mycursor = connection.cursor()


sql = "INSERT INTO trip (ind, tweet, retweets, favorites, created) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ind=%s;"

for count, tweet in enumerate(tweets):
    val = (count, tweet.full_text, tweet.retweet_count,
           tweet.favorite_count, tweet.created_at, count)
    try:
        mycursor.execute(sql, val)

    except Exception as error:
        print(error)
        break


connection.commit()
print(mycursor.rowcount, "record inserted.")