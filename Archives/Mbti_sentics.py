import pickle
from Sentics import Sentics
import re
import pandas as pd

# Docu https://amaiya.github.io/ktrain/text/index.html#ktrain.text.TransformerEmbedding
# https://github.com/amaiya/ktrain/blob/master/ktrain/text/preprocessor.py
# https://huggingface.co/distilbert-base-cased

# Import Data
Data = pd.read_csv('../Data/MBTI_full.csv')

# Get posts and matrix Labels
df = Data[['posts', 'type']]
df.reset_index(drop=True, inplace=True)
df = pd.concat([df, df.type.astype('str').str.get_dummies()], axis=1, sort=False)
df.drop('type', axis=1, inplace=True)
df.rename(columns={'posts': 'text'}, inplace=True)

Labels_names = df.columns.values[1:]
labels = df.loc[:, df.columns != 'text']

def moy_sentics(list_of_list):
    sent1 = sent2 = sent3 = sent4 = int(0)
    for elem in list_of_list:
        sent1 = (float(elem[0]) + sent1)
        sent2 = (float(elem[1]) + sent2)
        sent3 = (float(elem[2]) + sent3)
        sent4 = (float(elem[3]) + sent4)

    if sent1 != 0:
        sent1 = sent1 / len(list_of_list)
    elif sent2 != 0:
        sent2 = sent2 / len(list_of_list)
    elif sent3 != 0:
        sent3 = sent3 / len(list_of_list)
    elif sent4 != 0:
        sent4 = sent4 / len(list_of_list)
    return [sent1, sent2, sent3, sent4]

# Get Liwcs
LIWCs = Data.loc[:, ~Data.columns.isin(['type', 'posts', 'text_final'])]
print('Setup done \n')

All_moy_sentance_sentics = list()
count = 0

for text in df['text'].values:
    if count % 5 == 0:
        print(count)
    sentances = text.split('|||')
    every_sentance = list()
    for sentance in sentances:
        Without_Url = re.sub(r"http\S+", "", sentance)
        if Without_Url and not Without_Url.isspace():
            line = Sentics.Sentics(Without_Url)
            every_sentance.append(line.main())

    Moy_text = moy_sentics(every_sentance)
    All_moy_sentance_sentics.append(Moy_text)
    if count % 5 == 0:
        pickle.dump(All_moy_sentance_sentics, open('PKL_dump_sentics/' + str(count) + '.pkl', 'wb'))
    count +=1

pickle.dump(All_moy_sentance_sentics, open('../Data/PKL files/MBTI_sentics.pkl', 'wb'))
print('Done')