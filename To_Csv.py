import pickle
import pandas as pd

# Import the data
with open('Data/PKL files/Df.pkl', 'rb') as f:
    All_df = pickle.load(f)

# During the process of making the Df.pkl file something went wrong with the IMDBpy
# which ended up in a badly formatted DF. These next lines, rearrange the All_df to a much cleaner version of the DF.
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

# Those lines replace some artefacts that still appears in the "Role" column of the new Final_df DF.
Repl_str = {'\\Und R:difficult older sister':'undetermined',
            '\\agt':'agent',
            '\\Agt':'agent',
            'RU:':'undetermined',
            '\Voi\Her':'hero',
            '\\Und R:attractive high school sophomore':'undetermined',
            '\\Und R:worried father':'undetermined'}
Final_df['Role'] = Final_df['Role'].replace(Repl_str)

# The following lines produce the target values accordingly to the ontology made by Davide Picca. In which,
# we can found the archetypal personality profile of an Hero and a villain, which are:
# Hero = A.1 C.1 E.1 N.0 O.1 Vil = A.0 C.0 E.0 N.1 O.0
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

# Transform the list into Pandas Series
cEXT = pd.Series(E)
cNEU = pd.Series(N)
cAGR = pd.Series(A)
cCON = pd.Series(C)
cOPN = pd.Series(O)

# Add those Series to the Final_df dataframe
Final_df['cEXT'] = cEXT
Final_df['cNEU'] = cNEU
Final_df['cAGR'] = cAGR
Final_df['cCON'] = cCON
Final_df['cOPN'] = cOPN

# This line make sure no duplicate exist in the Final data frame
Final_df.drop_duplicates(inplace=True, ignore_index=True)

# Those lines save, for every role, a Csv version of the Final_df, has Y. Mehta's script use csv as input to pass on
# to the BERT transformer part of the models.
for elem in set(Final_df['Role']):
    _temp_df = Final_df[Final_df['Role']==elem]
    _temp_df = _temp_df[['Speech','cEXT','cNEU','cAGR','cCON','cOPN']]
    _tmp_csv = _temp_df.to_csv(index=True)
    with open(str(elem)+".csv", "w") as f:
        f.write(_tmp_csv)