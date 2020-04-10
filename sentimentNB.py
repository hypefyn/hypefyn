# %%
import json, pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import average_precision_score, confusion_matrix, classification_report


# %%

data = pd.read_json("data/sentiment140/sentiment140_clean_joint.json", orient='index')
print("Data Loaded")

#%%

train_text, test_text, train_label, test_label = train_test_split(data.tokens,data.label,test_size=0.2,random_state=100)

# %%
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),  # integer counts to weighted TF-IDF scores
    ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
])

# %%
pipeline.fit(data.tokens, data.label)
print("Model trained")

# test_pred = pipeline.predict(test_text)
# print(classification_report(test_label, test_pred), confusion_matrix(test_label, test_pred))

with open(".models/NB_trained.pickle","wb") as file:
    pickle.dump(pipeline,file)
print("Model exported")

# %%
tweets_clean = pd.read_json("data/tweets_clean_joint.json",orient='index')

tweets_text = tweets_clean.tokens.to_list()
tweets_pred = pipeline.predict(tweets_text)
tweets = pd.read_csv("data/all_tweets.csv")
tweets_sent = ["Pos" if sent==4 else "Neg" for sent in tweets_pred]
tweets_out = pd.concat([tweets, pd.DataFrame(tweets_sent,columns=["Prediction"])],axis=1)
tweets_out.to_csv("data/tweets_pred.csv")
print("Predictions generated")

