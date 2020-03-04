#%%
import nltk
nltk.download('ts')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

#%% Fetch data
from nltk.corpus import twitter_samples as ts

positive = ts.strings('positive_tweets.json')
negative = ts.strings('negative_tweets.json')
text = ts.strings('tweets.20150430-223406.json')

#%% Get tokens
pos_tokens = ts.tokenized('positive_tweets.json')

#%%
print(len(pos_tokens))
print(pos_tokens[0])

# %% Normalize the data
