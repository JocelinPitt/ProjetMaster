import pandas as pd

# Load the original data. Those data were loaded to get some information about them using the python console.
# Like, for example, the length the the speeches or the number of various element (movies, actor, characters, etc)
Data = pd.read_csv('../Data/DATA_full.csv')

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

UCI = pd.read_csv('../Data/cast.csv')