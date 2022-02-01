'''
This is a simple script that read a csv and transform it into a folder of individual text file. This operation was done
to get the LIWC value of the text. As the program that extract LIWC values take independent texts files as input.
'''

import pandas as pd
from tqdm import tqdm

Data = pd.read_csv('../Data/Data_essays/essays.csv')

Auth = Data['#AUTHID'].values.tolist()

for text, auth in tqdm(zip(Data['text'].values.tolist(), Auth)):
    with open('Data/Mairesse_text/'+str(auth), 'w') as f:
        f.write(text)
    f.close()
