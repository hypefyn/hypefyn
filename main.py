import pandas as pd
import os, argparse, pickle, json
from nlp.tokenizer import *
from nlp.hype import hype
import model.sentiment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', type=str)
    parser.add_argument('--psw', type=str)
    args = parser.parse_args()

    if args.user == None or args.psw == None:
        raise Exception("Cloud user and password missing")

    sentiment_path = "data/sentiment140/"

    if os.path.exists(sentiment_path+"sentiment140_clean_joint.json"):
        clean_data = pd.read_json("data/sentiment140/sentiment140_clean_joint.json", orient='index')
        clean_data.drop(clean_data[clean_data.label == 2].index,axis=0,inplace=True)
        print("Data Loaded")

    else:
        train_cols = ["polarity","id","date","query","user","text"]
        train_data = pd.read_csv(sentiment_path+"train.csv", encoding='latin',header=None,names=train_cols)
        val_data = pd.read_csv(sentiment_path+"test.csv", encoding='latin',header=None,names=train_cols)

        data = pd.concat([train_data, val_data],axis=0)
        print("Train data loaded")
        tokens = tokenize(data.text.to_list())
        print("Train data tokenized")

        tokens_clean = remove_noise(tokens)
        print("Train data cleaned")

        data_joint = join_tokens(tokens_clean)
        print("Train data joined")

        exp = dict_to_json(data.polarity.to_list(),data_joint)
        
        with open(sentiment_path + "sentiment140_clean_joint.json",'w') as o:
            json.dump(exp,o)
        print("Train data saved")
        
        clean_data = pd.DataFrame.from_dict(exp,
                                        orient='index')
        clean_data.drop(clean_data[clean_data.label == 2].index,axis=0,inplace=True)

    if os.path.exists(".models/model_trained.pickle"):
        with open(".models/model_trained.pickle","rb") as file:
            sentiment_model = pickle.load(file)
            print("Pretrained model loaded")
    else:
        print("Training new model...")
        sentiment_model = sentiment.train(clean_data)

        with open(".models/model_trained.pickle","wb") as file:
            pickle.dump(sentiment_model,file)
        print("Sentiment model trained and saved")

    final_hype = hype(args, sentiment_model)

    final_hype.to_csv("data/final_hype.csv",header=True,index=True)
    print("Final hype computed and saved")
