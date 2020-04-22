#%%
import pandas as pd
import numpy as np
import os


data = pd.DataFrame(columns=["text","retweets","favourites","timestamp"])

path = "data/tweets"

for folder in os.listdir(path):
    path = "data/tweets"
    path += "/" + folder
    for f in os.listdir(path):
        tweets = pd.read_csv(path+"/"+f,names=["ID","text","retweets","favourites","timestamp"]).drop(columns=["ID"])
        key = pd.DataFrame(np.array([folder for i in range(tweets.shape[0])]),columns=["keyword"])
        tweets = pd.concat([tweets,key],axis=1)
        data = pd.concat([data, tweets])

#%%
data.to_csv("data/all_tweets.csv",header=True)

