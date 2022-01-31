import pandas as pd
import Replacement
from imdb import IMDb
import pickle

ia = IMDb()

replacement_dic = Replacement.Replacement
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

'''
for movie in Data['Movie'].values:
    if movie not in replacement_dic.keys():
        Input = input(str(movie) + ':')
        if Input:
            replacement_dic[movie] = Input
        else:
            replacement_dic[movie] = movie
'''
Cast = pd.read_csv('Data/cast.csv')
replacement_string = {"\Adv": "adversary",
                      "\Agn": "agent",
                      "\Ani": "animal",
                      "\Bit": "bit role",
                      "\Cam": "cameo role",
                      "\Cro": "crook",
                      "\Grp": "group or band",
                      "\Her": "hero",
                      "\Inn": "innocent",
                      "\Lov": "love interest",
                      "\Sav": "savior",
                      "\Sci": "scientist",
                      "\Sdk": "sidekick",
                      "\Sus": "suspect",
                      "\Rul": "ruler",
                      "\Psy": "psychopath",
                      "\\Und": "undetermined",
                      "\Vmp": "vamp",
                      "\Vic": "victim",
                      "\Vil": "villain",
                      "\Voi": "voice only, narrator",
                      "\Wmp": "wimp"}

Cast['Role'] = Cast['Role'].replace(replacement_string)
Data['Rep'] = Data['Movie'].replace(replacement_dic)

Data['Rep'].apply(lambda x: x.title())
Sub_data = Data[Data['Rep'].isin(Cast['Movie'].tolist())]
Sub_cast = Cast[Cast['Movie'].isin(Sub_data['Rep'].tolist())]
Sm_subData = Sub_data[['Rep', 'Person', 'Speech']]
Sm_subCast = Sub_cast[['Movie', 'Actor', 'Role']]

Sm_subData['Person'] = Sm_subData['Person'].apply(lambda x: x.lower().title())

Movies_list = set(Sub_data['Rep'].tolist())  # len 152
heroAndVillain = Sm_subCast[Sm_subCast['Role'].isin(['villain', 'hero'])]  # len 25

Role_name = list()
'''for movie, actor in zip(heroAndVillain['Movie'].tolist(), heroAndVillain['Actor'].tolist()):
    Found = Sm_subData[Sm_subData['Rep'] == movie]
    print([per for per in Found['Person']])
    toadd = input(str(actor) + " in " + str(movie))
    Role_name.append(toadd)

with open('Df.pkl', 'rb') as f:
    OUT_df = pickle.load(f)'''

OUT_df = pd.DataFrame(columns=['Movie','Actor','Character','Speech','Role'])

for movie in set(Sm_subCast['Movie']):
    if movie not in set(OUT_df['Movie']):
        CastToFind = Sm_subCast[Sm_subCast['Movie'] == movie]
        DataToLink = Sm_subData[Sm_subData['Rep'] == movie]
        SearchMovie = ia.search_movie(movie)
        searchID = 0
        for mov in SearchMovie:
            if str(movie) == str(mov['title']):
                break
            else:
                ok = input("Is: " + str(movie) + " = " + str(mov['title'] + str(mov['year']) + "\nEmpty=True"))
                if not ok:
                    break
                else:
                    searchID += 1
        getMovie = ia.get_movie(SearchMovie[searchID].movieID)
        print('Working on: ' + getMovie['title'])
        print([per for per in DataToLink['Person']])
        for cast in CastToFind['Actor']:
            Character_name = str()
            try:
                People = ia.search_person(cast)[0].personID
                getCast = ia.get_person(People)
                if getCast in getMovie:
                    for elem in getMovie['cast']:
                        if People != elem.personID:
                            pass
                        else:
    
                            Character_name = elem.currentRole['name']
                if Character_name:
                    if Character_name in DataToLink['Person'].to_list():
                        Output = [movie, cast, Character_name,
                                  DataToLink.loc[DataToLink['Person'] == Character_name, 'Speech'].values,
                                  CastToFind.loc[CastToFind['Actor'] == cast, 'Role'].values]
                    else:
                        match = False
                        Part_Name = Character_name.split()
                        for part in Part_Name:
                            if part in DataToLink['Person'].to_list():
                                match = True
                                Output = [movie, cast, Character_name,
                                          DataToLink.loc[DataToLink['Person'] == part, 'Speech'],
                                          CastToFind.loc[CastToFind['Actor'] == cast, 'Role']]
                        if not match:
                            print(str(Character_name) + " not found...")
                            pass
                            '''link = input(str(Character_name))
                            if link:
                                Output = [movie, cast, Character_name,
                                          DataToLink.loc[DataToLink['Person'] == link, 'Speech'],
                                          CastToFind.loc[CastToFind['Actor'] == cast, 'Role']]
                            else:
                                pass'''
                    OUT_df.loc[len(OUT_df.index)] = Output
            except:
                pass
        print("Done with :" + str(movie))
        with open('Data/PKL files/Df.pkl', 'wb') as f:
            pickle.dump(OUT_df, f)

'''for movie, actor in zip(heroAndVillain['Movie'].tolist(), heroAndVillain['Actor'].tolist()):
    IaMovie = ia.get_movie(ia.search_movie(movie)[0].movieID)
    IaPerson = ia.get_person(ia.search_person(actor)[0].personID)
    count = 0
    idx = int()
    for pers in IaMovie['cast']:
        if pers['name'] == IaPerson['name']:
            idx = count
        else:
            count += 1

for Movie in set(heroAndVillain['Movie'].tolist()):

    _Ia_movie = ia.search_movie(Movie)
    MovID = _Ia_movie[0].movieID
    Ia_movie = ia.get_movie(MovID)
    HerVil_catchList = heroAndVillain[heroAndVillain['Movie'] == str(Movie)]
    for HerVil in HerVil_catchList['Actor']:
        _Ia_actor = ia.search_person(HerVil)
        ActID = _Ia_actor[0].personID
        Ia_actor = ia.get_person(ActID)
        if Ia_actor in Ia_movie:
            count = 0
            idx = int()
            for pers in Ia_movie['cast']:
                if pers['name'] == Ia_actor['name']:
                    idx = count
                else:
                    count += 1
            Role_name.append(Ia_movie['cast'][idx].currentRole['name'])
        else:
            print(Ia_actor['name'])
            print("not in " + str(Ia_movie['title']))

heroAndVillain['Person'] = Role_name

Speeches = list()
Movies = list()
Persons = list()
Roles = list()
for index, row in heroAndVillain.iterrows():
    catch = Sm_subData[(Sm_subData['Rep'] == row['Movie']) & (Sm_subData['Person'] == row['Person'])]
    if not catch.empty:
        Speeches.append(catch['Speech'].values[0])
        Movies.append(row['Movie'])
        Persons.append(row['Person'])
        Roles.append(row['Role'])

zipped = list(zip(Speeches, Movies, Persons, Roles))
df = pd.DataFrame(zipped, columns=['Speeches', 'Movies', 'Persons', 'Roles'])

# Hero = A.1 C.1 E.1 N.0 O.1
# Vil = A.0 C.0 E.0 N.1 O.0
O = list()
C = list()
E = list()
A = list()
N = list()
for index, row in df.iterrows():
    if row['Roles'] == 'villain':
        O.append('n')
        C.append('n')
        E.append('n')
        A.append('n')
        N.append('y')
    else:
        O.append('y')
        C.append('y')
        E.append('y')
        A.append('y')
        N.append('n')

cEXT = pd.Series(E)
cNEU = pd.Series(N)
cAGR = pd.Series(A)
cCON = pd.Series(C)
cOPN = pd.Series(O)

df['cEXT'] = cEXT
df['cNEU'] = cNEU
df['cAGR'] = cAGR
df['cCON'] = cCON
df['cOPN'] = cOPN

with open('DF_dump.pkl', 'wb') as f:
    pickle.dump(df, f)

to_keep = df[['Speeches','cEXT','cNEU','cAGR','cCON','cOPN']]'''
