'''
This script is an attempt to produce my own keras model. This version is the same as the All_together.py script but it
works on the essays.csv files which are Pennebaker et al. files. Those files are the same that were finally used to
train the models in the final version of this work.

This model is a 3 entry model that tried to predict the personalities of fictional characters based on their speeches,
The LIWC values and the Sentic values (sentimental analysis). It works on a MBTI classification

this script have changed a lot and this version is only the last "as it is" version of it

'''

import pickle
import numpy as np
from keras_preprocessing.sequence import pad_sequences
from sklearn import model_selection
import pandas as pd
from tensorflow import keras

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

# Get Liwcs
LIWCs = Data.loc[:, ~Data.columns.isin(['type', 'posts', 'text_final'])]
print('Setup done \n')

# Pickle Load
objectRep = open("../Data/PKL files/embed.pkl", "rb")
Embd_bert = pickle.load(objectRep)
objectRep.close()

objectRep = open("../Data/PKL files/MBTI_sentics.pkl", "rb")
Mbti_sentics = pickle.load(objectRep)
objectRep.close()
print('Pickle load \n')

# Reforme x, y from various input
Pad_bert = list()

for pad in Embd_bert:
    max_length = 256
    padded_docs = pad_sequences(pad, maxlen=max_length, padding='post')
    Pad_bert.append(padded_docs[0, :, :])

MBTI = pd.DataFrame(Mbti_sentics)

train_bert, test_bert, train_label, test_label, train_liwc, test_liwc, train_sentic, test_sentic = model_selection.train_test_split(
    Pad_bert, labels, LIWCs, MBTI, test_size=0.2)

train_bert = np.stack(train_bert, axis=0)
test_bert = np.stack(test_bert, axis=0)
print('X Y sets')

# Model bert
input_bert = keras.layers.Input(shape=(256, 768), name='Bert')
flat_bert = keras.layers.Flatten()(input_bert)
Reduce_bert = keras.layers.Dense(512, activation='relu', name='Reduced_bert')(flat_bert)

# Model sentics
input_sentics = keras.layers.Input(shape=(4), name='Sentics')

# Model LIWCs
input_liwcs = keras.layers.Input(shape=(95), name='Liwc')

# Model Concat to out
Concat = keras.layers.concatenate([Reduce_bert, input_sentics, input_liwcs], axis=1)
Dense_1 = keras.layers.Dense(512, activation='relu')(Concat)
DropOut = keras.layers.Dropout(.2)(Dense_1)
Dense_2 = keras.layers.Dense(128, activation='relu')(DropOut)
Output = keras.layers.Dense(16, activation='sigmoid')(Dense_2)

# Model optimizer
Ada_delta = keras.optimizers.Adadelta(learning_rate=0.001, rho=0.95, epsilon=1e-07, name="Adadelta")

# Model init
model = keras.models.Model(inputs=[input_bert, input_sentics, input_liwcs], outputs=Output)
model.get_layer('Reduced_bert').trainable = False
model.compile(loss="binary_crossentropy", optimizer='Adadelta', metrics=["accuracy"])
model.summary()

# Fit Model
history = model.fit(x=[train_bert, train_sentic, train_liwc],
                    y=train_label,
                    validation_data=([test_bert, test_sentic, test_liwc],
                                     test_label),
                    epochs=10,
                    batch_size=32,
                    verbose=1)
