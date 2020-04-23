# Credits to Shaumik Daityari https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk

#%%
import nltk
nltk.download('ts')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

#%% Fetch data
from nltk.corpus import twitter_samples as ts

positive = ts.strings('positive_tweets.json')
negative = ts.strings('negative_tweets.json')
text = ts.strings('tweets.20150430-223406.json')

#%% Get tokens
tw_tokens = ts.tokenized('positive_tweets.json')

#%%
print(len(tw_tokens))
print(tw_tokens[0])

# %% Add a tag to each token and normalize forms
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

# print(pos_tag(tw_tokens[0]))

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

# print(lemmatize_sentence(tw_tokens[0]))

# %% Remove noise with normalization included
import re, string
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

# print(remove_noise(tw_tokens[0]))
# print(remove_noise(tw_tokens[0], stop_words))

#%%  Remove noise from data

pos_tw_tokens = ts.tokenized('positive_tweets.json')
neg_tw_tokens = ts.tokenized('negative_tweets.json')

pos_tokens_list = []
neg_tokens_list = []

for tokens in pos_tw_tokens:
    pos_tokens_list.append(remove_noise(tokens, stop_words))
for tokens in neg_tw_tokens:
    neg_tokens_list.append(remove_noise(tokens, stop_words))

print(pos_tw_tokens[500])
print(pos_tokens_list[500])
# %% Determine word density

from nltk import FreqDist

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

all_pos_words = get_all_words(pos_tokens_list)

freq_dist_pos = FreqDist(all_pos_words)
print(freq_dist_pos.most_common(10))

# %% Convert tokens to a dictionary

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

pos_token_for_model = get_tweets_for_model(pos_tokens_list)
neg_token_for_model = get_tweets_for_model(neg_tokens_list)


# %% Split dataset in train and test data
import random

pos_dataset = [(tweet_dict, "Positive") for tweet_dict in pos_token_for_model]
neg_dataset = [(tweet_dict, "Negative") for tweet_dict in neg_token_for_model]

dataset = pos_dataset + neg_dataset

random.shuffle(dataset)
print(len(dataset))
#%%
train_data = dataset[:7000]
test_data = dataset[7000:]

# %% Building a classifier model: Naive Bayes

from nltk import classify
from nltk import NaiveBayesClassifier
classifier = NaiveBayesClassifier.train(train_data)

print("Accuracy is:", classify.accuracy(classifier, test_data))

print(classifier.show_most_informative_features(10))



# %%
