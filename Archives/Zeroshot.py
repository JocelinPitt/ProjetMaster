'''
This is an small attempt to perform Zero-shot learning onto my data, using the Ktrain package.
This approach simply doesn't work for personality detection.
'''
import os
import ktrain
import pandas as pd

from ktrain.text.zsl import ZeroShotClassifier

zsl = ZeroShotClassifier()
labels=['cEXT','cNEU','cAGR','cCON','cOPN']


Data = pd.read_csv('../Data/Data_essays/essays.csv')

texts = Data['text']
Labels = Data['cEXT','cNEU','cAGR','cCON','cOPN']

y_true  = Labels[:10]

for x in texts[:10]:
    out = zsl.predict(x, labels=labels, include_labels=True)