'''
Those are discarded codes made to perform the same output as the Imdb.py script
This part was used to reload the OUT_df file as this process can be very long and could not be done in a single
time Others changes were in place at that time but those no longer exists as they have been removed since this
process is done.
'''
for movie, actor in zip(heroAndVillain['Movie'].tolist(), heroAndVillain['Actor'].tolist()):
    Found = Sm_subData[Sm_subData['Rep'] == movie]
    print([per for per in Found['Person']])
    toadd = input(str(actor) + " in " + str(movie))
    Role_name.append(toadd)

with open('Df.pkl', 'rb') as f:
    OUT_df = pickle.load(f)

for movie, actor in zip(heroAndVillain['Movie'].tolist(), heroAndVillain['Actor'].tolist()):
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
