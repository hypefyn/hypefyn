# %%
import json

# %%
with open("data/sentiment140/train_clean_joint.json",'r') as t:
    train = json.load(t)
with open("data/sentiment140/val_clean_joint.json",'r') as v:
    test = json.load(v)

# %%

k = str(len(train))

for d in test.values():
    train[k] = d
    k = str(int(k)+1)

# %%
with open("data/sentiment140/sentiment140_clean_joint.json",'w') as v:
    json.dump(train,v)
    