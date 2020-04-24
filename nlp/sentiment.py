# %%
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# %%

# data = pd.read_json("data/sentiment140/sentiment140_clean_joint.json", orient='index')
# data.drop(data[data.label == 2].index,axis=0,inplace=True)
# print("Data Loaded")

# #%%

# train_text, test_text, train_label, test_label = train_test_split(data.tokens,data.label,test_size=0.2,random_state=100)
# print("Splits created")

# # %%
# pipeline = Pipeline([
#     ('tfidf', TfidfVectorizer()),  # integer counts to weighted TF-IDF scores
#     ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
# ])

# #%%
# model_cv = GridSearchCV(pipeline,
#                         param_grid={'classifier__l1_ratio':[0,0.5,1],
#                                     'classifier__C':[1,10]},
#                         n_jobs=-1)
# print("Training")
# model_cv.fit(train_text, train_label)
# print("Testing")
# best_pred = model_cv.best_estimator_.predict(test_text)
# print(model_cv.best_params_,"\n", classification_report(test_label, best_pred), confusion_matrix(test_label, best_pred))


def train(data):
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=10)),
    ])

    pipeline.fit(data.tokens, data.label)

    return pipeline





# %%
# print("Training the model...")
# pipeline.fit(train_text, train_label)
# print("Model trained")

# test_pred = pipeline.predict(test_text)
# print(classification_report(test_label, test_pred), confusion_matrix(test_label, test_pred))

# with open(".models/NB_trained.pickle","wb") as file:
#     pickle.dump(pipeline,file)
# print("Model exported")

# %% Prediction
# tweets_clean = pd.read_json("data/tweets_clean_joint.json",orient='index')

# tweets_text = tweets_clean.tokens.to_list()
# tweets_pred = pipeline.predict(tweets_text)
# tweets = pd.read_csv("data/all_tweets.csv")
# tweets_sent = ["Pos" if sent==4 else "Neg" for sent in tweets_pred]
# tweets_out = pd.concat([tweets, pd.DataFrame(tweets_sent,columns=["prediction"])],axis=1)
# tweets_out.to_csv("data/tweets_pred.csv")
# print("Predictions generated")

