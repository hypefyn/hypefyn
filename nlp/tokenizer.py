#%% Libraries
import re, string, nltk
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords

# %% Functions
def tokenize(list):
    tknzr = TweetTokenizer()
    tokens_list = []
    for text in list:
        tokens_list.append(tknzr.tokenize(text))
    return tokens_list

def remove_noise(tokens_list, stop_words = stopwords.words('english'), keep_emph=False):

    tokens = []
    for tweet_tokens in tokens_list:
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

            if keep_emph:
                punct = re.sub("[!?]","", string.punctuation)
            else:
                punct = string.punctuation

            if len(token) > 0 and token not in punct and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        tokens.append(cleaned_tokens)
    return tokens

def join_tokens(tokens_list):
    joint = []
    for tweet in tokens_list:
        tw = ""
        for word in tweet:
            tw += " " + word
        joint.append(tw)
    return joint

def dict_to_json(label, tokens_clean):
    exp = {}
    for ind, toks in enumerate(tokens_clean):
        t = {}
        t["label"] = label[ind]
        t["tokens"] = toks
        exp[ind] = t
    return exp

