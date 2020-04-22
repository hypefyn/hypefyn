import os
import sys
import codecs
import csv
import pymysql
import GetOldTweets3 as got

user = 'pietro'
psw = 'test123'

# remaining: data march 22nd to march 31st
# amazon $amzn corona covid delta $dal google $goog 
# netflix $nflx novartis $nvs pfizer $pfe tesla $tsla tripadvisor $trip uber $uber zoom $zm
# to distinguish between uber and $uber I did q="uber -$uber -filter:retweets"

# would you please do the inserts for 
# 1. setQuerySearch delta insert into delta for 2020-03-22, 2020-03-23, ..., 2020-03-31 and 
# 2. setQuerySearch zoom insert into zoom for 2020-03-22, 2020-03-23, ..., 2020-03-31 and if you can 
# 3. setQuerySearch corona insert into corona for 2020-03-22, 2020-03-23, ..., 2020-03-31

# corona all
# delta only 31

for key in ["tripadvisor","pfizer"]:
    day = "2020-03-22"
    while True:
        if day == "2020-03-31":
            day2 = "2020-04-01"
        elif day == "2020-04-01":
            print("\n Finished!")
            break
        else:
            day2 = day[:-2] + str(int(day[-2:]) + 1)
        print(f"Collecting tweets from {key} for {day}")

        tweetCriteria=got.manager.TweetCriteria().setQuerySearch(key).setSince(day).setUntil(day2).setMaxTweets(1000).setEmoji("unicode").setLang("en")
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)

        connection = pymysql.connect(
            host="34.74.21.31", user=user, password=psw, db="Hypefyn", charset='utf8mb4', use_unicode=True)
        mycursor = connection.cursor()

        sql = "INSERT INTO " + key + " (ind, tweet, retweets, favorites, created) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ind=%s;"

        for count, tweet in enumerate(tweets):
            val = (count, tweet.text, tweet.retweets,
                tweet.favorites, tweet.date, count)
            try:
                mycursor.execute(sql, val)

            except Exception as error:
                print(error)
                break

        connection.commit()
        print(mycursor.rowcount, "record inserted.")

        day = day2