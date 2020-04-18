# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%
tweets = pd.read_csv("data/tweets_pred.csv")
tweets = tweets.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])

# %%

def round_time(column, freq = 'D'):
    time_rounded = []
    for time in column.to_numpy():
        time = pd.Timestamp(time).round(freq=freq)
        time_rounded.append(time)
    return pd.DataFrame(time_rounded)

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

def get_hype(df, grouping, weights=(1,1,1), delta_t=1):

    # time_delta = pd.Timedelta(minutes=delta_t)
    hype = {}
    i = 0

    for group in grouping:
        keys = grouping[group]
        tweets_group = pd.DataFrame()
        for key in keys:
            tweets_group = pd.concat([tweets_group,tweets[tweets.keyword == key].copy()])
        while tweets_group.shape[0] != 0:
            time_start = tweets_group.timestamp.min()
            tw = tweets_group[tweets_group.timestamp <= time_start]# + time_delta]
            pos_hype, neg_hype = hype_scores(tw, weights)
            tweets_group.drop(tw.index,inplace=True)
            hype[i] = [group,
                        str(time_start),# + time_delta/2),
                        pos_hype,neg_hype]
            i += 1
    
    return pd.DataFrame.from_dict(hype,orient='index',columns=["keyword","timestamp","pos_hype","neg_hype"])

# %%

tweets.timestamp = round_time(tweets.timestamp)

grouping = {'tesla':['$TSLA','tesla'],'corona':["corona","COVID"],'zoom':['$ZM']}

hype = get_hype(tweets, grouping)

hype_out = pd.DataFrame(hype.timestamp.unique(),columns=['datetime'])

for key in grouping:
    x = (hype[hype.keyword==key].pos_hype - hype[hype.keyword==key].neg_hype).to_numpy()
    hype_out[key+"_hype"] = [np.log2(v) if v > 0 else -np.log2(-v) for v in x] 

hype_out.to_csv("data/tweets_hype.csv",header=True,index=False)
