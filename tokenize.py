#%% Libraries
import re, string, nltk, json
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

# %% Functions
def tokenize(list):
    tknzr = TweetTokenizer()
    tokens_list = []
    for text in list:
        tokens_list.append(tknzr.tokenize(text))
    return tokens_list

def remove_noise(tokens_list, stop_words = (), keep_emph=False):

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

def dict_to_json(label, tokens_clean, output_path):
    exp = {}
    for ind, toks in enumerate(tokens_clean):
        t = {}
        t["label"] = label[ind]
        t["tokens"] = toks
        exp[ind] = t
    with open(output_path,'w') as o:
        json.dump(exp,o)

#%% 

train_path = "data/sentiment140/train.csv"
val_path = "data/sentiment140/test.csv"
tweets_path = "data/all_tweets.csv"

train_cols = ["polarity","id","date","query","user","text"]
train_data = pd.read_csv(train_path, encoding='latin',header=None,names=train_cols)
val_data = pd.read_csv(val_path, encoding='latin',header=None,names=train_cols)

# tweets_data = pd.read_csv(tweets_path)

train_tokens = tokenize(train_data.text.to_list())
val_tokens = tokenize(val_data.text.to_list())
# tweets_tokens = tokenize(tweets_data.text.to_list())

stop_words = stopwords.words('english')



train_tokens_clean = remove_noise(train_tokens[:1000], stop_words)
# val_tokens_clean = remove_noise(val_tokens, stop_words)
# tweets_tokens_clean = remove_noise(tweets_tokens, stop_words)



train_joint = join_tokens(train_tokens_clean)

d = dictionalize(train_data.iloc[:1000].polarity.to_list(),train_tokens_clean)


