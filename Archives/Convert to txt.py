import pandas as pd
from tqdm import tqdm

Data = pd.read_csv('../Data/Data_essays/essays.csv')

Auth = Data['#AUTHID'].values.tolist()

for text, auth in tqdm(zip(Data['text'].values.tolist(), Auth)):
    with open('Data/Mairesse_text/'+str(auth), 'w') as f:
        f.write(text)
    f.close()
