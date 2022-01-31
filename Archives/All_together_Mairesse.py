import pickle
import numpy as np
from keras_preprocessing.sequence import pad_sequences
from sklearn import model_selection
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import StratifiedKFold

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

Labels_cExt = Labels['cEXT'].to_numpy()

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

pd_bert = np.asarray(Pad_bert)

train_bert, test_bert, train_label, test_label, train_LIWC, test_LIWC, train_sentic, test_sentic = \
    model_selection.train_test_split(Pad_bert, Labels_cExt, LIWC, Sentics, test_size=0.2)

train_bert = np.stack(train_bert, axis=0)
test_bert = np.stack(test_bert, axis=0)
print('X Y sets')

print(type(Pad_bert))

skf = StratifiedKFold(n_splits=10, shuffle=False)
for train_index, test_index in skf.split(pd_bert, Labels_cExt):
    x_train, x_test = pd_bert[train_index], pd_bert[test_index]
    y_train, y_test = Labels_cExt[train_index], Labels_cExt[test_index]

    y_train = tf.keras.utils.to_categorical(y_train, num_classes=5)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes=5)

    model = tf.keras.models.Sequential()

    # define the neural network architecture
    model.add(
        tf.keras.layers.Dense(50, input_dim=768, activation="relu")
    )
    model.add(tf.keras.layers.Dense(5))

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
        metrics=["mse", "accuracy"],
    )
    history = model.fit(
        x_train,
        y_train,
        epochs=10,
        batch_size=32,
        validation_data=(x_test, y_test),
        verbose=0,
    )


# Model bert
#input_bert = keras.layers.Dense(50, input_dim=(512, 768), name='Bert')
'''
input_bert = keras.layers.Input(shape=(512, 768), name='Bert')
flat_bert = keras.layers.Flatten()(input_bert)
Reduce_bert = keras.layers.Dense(512, activation='relu', name='Reduced_bert')(flat_bert)

# Model sentics
input_sentics = keras.layers.Input(shape=(5), name='Sentics')

# Model LIWCs
input_liwcs = keras.layers.Input(shape=(93), name='Liwc')

# Model Concat to out
Concat = keras.layers.concatenate([input_bert, input_liwcs, input_sentics], axis=1)
#Concat = keras.layers.concatenate([Reduce_bert, input_liwcs, input_sentics], axis=1)
Dense_1 = keras.layers.Dense(50)(Concat)
#Output = keras.layers.Dense(1)(Dense_1)
DropOut = keras.layers.Dropout(.2)(Dense_1)
Dense_2 = keras.layers.Dense(128, activation='relu')(DropOut)
Output = keras.layers.Dense(1, activation='softmax')(Dense_2)

# Model optimizer
Ada_delta = keras.optimizers.Adadelta(learning_rate=0.001, rho=0.95, epsilon=1e-07, name="Adadelta")

# Model init
model = keras.models.Model(inputs=[input_bert, input_liwcs, input_sentics], outputs=Output)
model.get_layer('Reduced_bert').trainable = False
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer='Adadelta',
              metrics=["mse", "accuracy"])
model.summary()'''
print("model made !")

# Fit Model
history = model.fit(x=[train_bert, train_LIWC, train_sentic],
                    y=train_label,
                    validation_data=([test_bert, test_LIWC, test_sentic],
                                     test_label),
                    epochs=10,
                    batch_size=64,
                    verbose=1)
