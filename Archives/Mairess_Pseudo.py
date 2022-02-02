'''
This script is an attempt to perform pseudo-labeling onto my dataset. This file calls the Pseudo_Label_class.py.
This attempt wasn't considered for long and therefore a lot of errors are still present in here.
'''

import Pseudo_Label_class as Psdo
import pickle
import numpy as np
from keras_preprocessing.sequence import pad_sequences
from sklearn import model_selection
import pandas as pd
import tensorflow as tf
from tensorflow import keras

# Import Data
Data = pd.read_csv("../Data/Data_essays/essays.csv")
Sentics = pd.read_csv('../Data/Data_essays/essays_senticnet.csv')

LIWC = pd.read_csv('../Data/Data_essays/essays_LIWC.csv')
LIWC.rename(columns={'Filename': '#AUTHID'}, inplace=True)

All_data = Data.merge(Sentics, on="#AUTHID", how="left").merge(LIWC, on='#AUTHID', how='left')

LIWC.drop(['#AUTHID', 'Segment'], axis=1, inplace=True)
# Get posts and matrix Labels
Labels = All_data[['cEXT', 'cNEU', 'cAGR', 'cCON', 'cOPN']]
Sentics = All_data[['pleasantness_value', 'attention_value', 'sensitivity_value', 'aptitude_value', 'polarity_value']]

replace_values = {'n': np.int64(0), 'y': np.int64(1)}
Labels = Labels.replace(replace_values)
Labels.fillna(np.int64(0))
Labels_names = Labels.columns.values

print('Setup done \n')

# Pickle Load
objectRep = open('../Data/PKL files/Mairesse_embed.pkl', 'rb')
Embd_bert = pickle.load(objectRep)
objectRep.close()

# Reforme x, y from various input
Pad_bert = list()

for pad in Embd_bert:
    max_length = 512
    padded_docs = pad_sequences(pad, maxlen=max_length, padding='post')
    Pad_bert.append(padded_docs[0, :, :])

train_bert, test_bert, train_label, test_label, train_LIWC, test_LIWC, train_sentic, test_sentic = \
    model_selection.train_test_split(Pad_bert, Labels, LIWC, Sentics, test_size=0.2)

train_bert = np.stack(train_bert, axis=0)
test_bert = np.stack(test_bert, axis=0)
print('X Y sets')
