import pandas as pd
import Replacement
from imdb import IMDb
import pickle

# Calling IMDBpy
ia = IMDb()

# Loading dataset and dictionary
replacement_dic = Replacement.Replacement
Data = pd.read_csv('Data/DATA_full.csv')

# The following section works on the filename column. It separate the name of the movie and the name of the character
# into two different columns
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

# This function add the newly created columns to de DF.
Data['Movie'] = movies
Data['Person'] = persons

# This section is no longer useful as it was used during the creation of the replacement dictionary.
# The goal here is to rename every movies to increased the chances of the following code to found a match.
'''
for movie in Data['Movie'].values:
    if movie not in replacement_dic.keys():
        Input = input(str(movie) + ':')
        if Input:
            replacement_dic[movie] = Input
        else:
            replacement_dic[movie] = movie
'''

# This section load the Cast data frame and another replacement dictionary which transform the roles name into a more
# readable version
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

# The replacement dictionaries are applied here
Cast['Role'] = Cast['Role'].replace(replacement_string)
Data['Rep'] = Data['Movie'].replace(replacement_dic)

# This section match the two dataframes based on their movie title. When the matching is done, we only keeps the
# columns that contains the information that we need.
Data['Rep'].apply(lambda x: x.title())
Sub_data = Data[Data['Rep'].isin(Cast['Movie'].tolist())]
Sub_cast = Cast[Cast['Movie'].isin(Sub_data['Rep'].tolist())]
Sm_subData = Sub_data[['Rep', 'Person', 'Speech']]
Sm_subCast = Sub_cast[['Movie', 'Actor', 'Role']]

Sm_subData['Person'] = Sm_subData['Person'].apply(lambda x: x.lower().title())

# This variable contains a set of every movies
Movies_list = set(Sub_data['Rep'].tolist())  # len 152

# this variable contains only villain et heros.
heroAndVillain = Sm_subCast[Sm_subCast['Role'].isin(['villain', 'hero'])]  # len 25

# This is the last version of the script that try to match both dataframes
Role_name = list()

OUT_df = pd.DataFrame(columns=['Movie','Actor','Character','Speech','Role'])

for movie in set(Sm_subCast['Movie']):
    if movie not in set(OUT_df['Movie']):
        CastToFind = Sm_subCast[Sm_subCast['Movie'] == movie]
        DataToLink = Sm_subData[Sm_subData['Rep'] == movie]

        # this function return a list of objects based on the movie title
        SearchMovie = ia.search_movie(movie)
        searchID = 0

        # This part search for the movie
        for mov in SearchMovie:
            # If the title is a perfect match
            if str(movie) == str(mov['title']):
                break

            # Otherwise the program ask for user validation
            else:
                ok = input("Is: " + str(movie) + " = " + str(mov['title'] + str(mov['year']) + "\nEmpty=True"))
                if not ok:
                    break
                else:
                    searchID += 1

        # This function get information about the movie using his Id. We get the id among the previous list
        getMovie = ia.get_movie(SearchMovie[searchID].movieID)
        print('Working on: ' + getMovie['title'])

        # The program will print the list of characters present in the Data DF.
        # This will be use full if the program doesn't get automatically a match
        print([per for per in DataToLink['Person']])

        # This will loop on every actor available in the UCI Dataset for a given movie
        for cast in CastToFind['Actor']:
            Character_name = str()
            # The first thing to do is to get their character name as written in IMBD data base
            try:
                People = ia.search_person(cast)[0].personID
                getCast = ia.get_person(People)
                if getCast in getMovie:
                    for elem in getMovie['cast']:
                        if People != elem.personID:
                            pass
                        else:
                            Character_name = elem.currentRole['name']

                # If a character name was found
                if Character_name:
                    # If the character name is the same as the one in our data frame we save the information we need
                    # in a variable called Output
                    if Character_name in DataToLink['Person'].to_list():
                        Output = [movie, cast, Character_name,
                                  DataToLink.loc[DataToLink['Person'] == Character_name, 'Speech'].values,
                                  CastToFind.loc[CastToFind['Actor'] == cast, 'Role'].values]
                    else:
                        # Otherwise we try to split IMBD's name and try to match every part with the names we have
                        match = False
                        Part_Name = Character_name.split()
                        for part in Part_Name:
                            if part in DataToLink['Person'].to_list():
                                match = True
                                # If found : we save the information in the Output variable
                                Output = [movie, cast, Character_name,
                                          DataToLink.loc[DataToLink['Person'] == part, 'Speech'],
                                          CastToFind.loc[CastToFind['Actor'] == cast, 'Role']]
                        # If we still haven't match the character's name. The program will ask for the user's help
                        if not match:
                            print(str(Character_name) + " not found...")
                            link = input(str(Character_name))
                            if link:
                                Output = [movie, cast, Character_name,
                                          DataToLink.loc[DataToLink['Person'] == link, 'Speech'],
                                          CastToFind.loc[CastToFind['Actor'] == cast, 'Role']]
                            else:
                                pass
                    OUT_df.loc[len(OUT_df.index)] = Output
            except:
                pass
        print("Done with :" + str(movie))
        # The program save after every movie, because as the user is frequently ask to do some input this process can
        # very very long.
        with open('Data/PKL files/Df.pkl', 'wb') as f:
            pickle.dump(OUT_df, f)