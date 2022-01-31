import pickle
import pandas as pd

with open('Data/PKL files/DF_dump.pkl', 'rb') as f:
    df = pickle.load(f)

with open('Data/PKL files/Df.pkl', 'rb') as f:
    All_df = pickle.load(f)

All_movie = []
All_actor = []
All_Character = []
All_Speech = []
All_Role = []
for indice, row in All_df.iterrows():
    All_movie.append(row['Movie'])
    All_actor.append(row['Actor'])
    All_Character.append(row['Character'])
    if type(row['Speech']) is pd.Series:
        All_Speech.append(row['Speech'].values[0])
    else:
        All_Speech.append(row['Speech'][0])
    if type(row['Role']) is pd.Series:
        All_Role.append(row['Role'].values[0])
    else:
        All_Role.append(row['Role'][0])


Final_df = pd.DataFrame()
Final_df['Movie'] = All_movie
Final_df['Actor'] = All_actor
Final_df['Character'] = All_Character
Final_df['Speech'] = All_Speech
Final_df['Role'] = All_Role

Repl_str = {'\\Und R:difficult older sister':'undetermined',
            '\\agt':'agent',
            '\\Agt':'agent',
            'RU:':'undetermined',
            '\Voi\Her':'hero',
            '\\Und R:attractive high school sophomore':'undetermined',
            '\\Und R:worried father':'undetermined'}

Final_df['Role'] = Final_df['Role'].replace(Repl_str)

Data = pd.read_csv('Data/DATA_full.csv')

Data_filename = Data['Filename']
movies = []
persons = []

for filename in Data_filename:
    x = filename.split(' ')
    if len(x) == 2:
        person = x[1][:-4].lower()
        persons.append(person)
        movie = x[0][:-4]
        movies.append(movie)
    else:
        movie = x[0][:-4]
        movies.append(movie)
        x.pop(0)
        person = ' '.join(x)
        persons.append(person[:-4])

Data['Movie'] = movies
Data['Person'] = persons

Leng = []
for spe in Data['Speech'].values:
    _len = len(spe)
    Leng.append(_len)

Data['Lenght'] = Leng

UCI = pd.read_csv('Data/cast.csv')

# Hero = A.1 C.1 E.1 N.0 O.1
# Vil = A.0 C.0 E.0 N.1 O.0
O = list()
C = list()
E = list()
A = list()
N = list()
for index, row in Final_df.iterrows():
    if row['Role'] == 'villain':
        O.append('n')
        C.append('n')
        E.append('n')
        A.append('n')
        N.append('y')
    elif row['Role'] == 'hero':
        O.append('y')
        C.append('y')
        E.append('y')
        A.append('y')
        N.append('n')
    else:
        O.append('n')
        C.append('n')
        E.append('n')
        A.append('n')
        N.append('n')

cEXT = pd.Series(E)
cNEU = pd.Series(N)
cAGR = pd.Series(A)
cCON = pd.Series(C)
cOPN = pd.Series(O)

Final_df['cEXT'] = cEXT
Final_df['cNEU'] = cNEU
Final_df['cAGR'] = cAGR
Final_df['cCON'] = cCON
Final_df['cOPN'] = cOPN

Final_df.drop_duplicates(inplace=True, ignore_index=True)

for elem in set(Final_df['Role']):
    _temp_df = Final_df[Final_df['Role']==elem]
    _temp_df = _temp_df[['Speech','cEXT','cNEU','cAGR','cCON','cOPN']]
    _tmp_csv = _temp_df.to_csv(index=True)
    with open(str(elem)+".csv", "w") as f:
        f.write(_tmp_csv)