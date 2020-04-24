import argparse
import pymysql
import GetOldTweets3 as got

parser = argparse.ArgumentParser()
parser.add_argument('--user', type=str)
parser.add_argument('--psw', type=str)
args = parser.parse_args()

if args.user == None or args.psw == None:
    raise Exception("Cloud user and password missing")

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
            host="34.74.21.31", user=args.user, password=args.psw, db="Hypefyn", charset='utf8mb4', use_unicode=True)
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