# %% Import true sample twwets

with open("data/ZM.txt", encoding='utf8') as zm:
    l = []
    for i in range(3):
        line = zm.readline()
        l.append(line)
        print(line,l)

#%% 

l[0].startswith("RT")