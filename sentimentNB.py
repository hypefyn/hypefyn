# %%
import json
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

# %%
with open("data/sentiment140/train_clean_joint.json",'r') as t:
    train = json.load(t)
with open("data/sentiment140/val_clean_joint.json",'r') as v:
    test = json.load(v)

# %%
pipeline = Pipeline([
    ('vectorizer',HashingVectorizer(n_features=2**16)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
])
