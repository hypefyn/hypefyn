#%% Libraries
import re, string, nltk, json
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

# %%
sentiment_path = drive_path + "data/sentiment140/"
tweets_path = drive_path + "data/"

stop_words = stopwords.words('english')

train_cols = ["polarity","id","date","query","user","text"]
train_data = pd.read_csv(sentiment_path+"train.csv", encoding='latin',header=None,names=train_cols)
val_data = pd.read_csv(sentiment_path+"test.csv", encoding='latin',header=None,names=train_cols)

tweets_data = pd.read_csv(tweets_path+"all_tweets.csv")
print("Data Loaded")

train_tokens = tokenize(train_data.text.to_list())
val_tokens = tokenize(val_data.text.to_list())
tweets_tokens = tokenize(tweets_data.text.to_list())
print("Data Tokenized")

train_tokens_clean = remove_noise(train_tokens, stop_words)
print("Train data cleaned")
val_tokens_clean = remove_noise(val_tokens, stop_words)
print("Val data cleaned")
tweets_tokens_clean = remove_noise(tweets_tokens, stop_words)
print("Tweets data cleaned")

train_joint = join_tokens(train_tokens_clean)
print("Train data joined")
val_joint = join_tokens(val_tokens_clean)
print("Val data joined")
tweets_joint = join_tokens(tweets_tokens_clean)
print("Tweets data joined")


dict_to_json(train_data.polarity.to_list(),train_joint, output_path=sentiment_path + "train_clean_joint.json")
print("Train data exported")
dict_to_json(val_data.polarity.to_list(),val_joint, output_path=sentiment_path + "val_clean_joint.json")
print("Val data exported")
dict_to_json(tweets_data.keyword.to_list(),tweets_joint, output_path=tweets_path + "tweets_clean_joint.json")
print("Tweets data exported")
