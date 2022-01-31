# Projet Master
This repository is a compilation of scripts that i used during my Master's project.

The goal of those scripts are to perform personnality detection on fictional caracters.
The personnality dectection algorithms are made following Y. Mehta procedure [(See Y. Mehta's Github)](https://github.com/yashsmehta/personality-prediction).

In the Archives section, you can find many attempts to conduct personality detection. Those include the works i've done using google colabs, but also some tests i made with sentiment analysis
[(See SenticNet web site)](https://www.sentic.net/). In this directory, you can also find many attempts that I've done to build my own Keras models.

The files placed in the root directory are the one that i finaly used in the final form of my Master's Project. Those are :

## Imdb.py
This file goal is to link two dataframe. UCI's cast.html from their Movie Data Set [(See UCI's Machine learning repository web page)](https://archive.ics.uci.edu/ml/datasets/Movie) and 
a Dataframe made by myself in another class work. Those dataframes are to be linked based on their movie title and the fictional character's names, which isn't contained in the UCI dataframe.
To do so, this script have been written using the IMDBpy package.

## Predict.py
This file is a simple script that call trained models to perform personality prediction on the fictional characters both present in the two dataframes previously mentioned.
This script is used to call Keras functions evalute et predict and produce confusion Matrix. The script includ a variable call "path" that should be changed in order to work.

## Replacement.py
This file is a python dictionary that was made to transform my personal dataframe. 
Those transformations are made to help the works of the Imdb.py script. It change the movies names accordingly to IMDB catalogue.

## DATAs
Due to file size restriction on Github, no data file were include on this repository. Those can be download on the Zenodo sandbox with the following links:
* [Multiple personality data set](https://sandbox.zenodo.org/record/1004709)
* [Movies speeches by narratives role Dataset](https://sandbox.zenodo.org/record/1004703)
* [Pennebaker et al. // Mairesse et al. // personality dataset, Associated LIWC and Sentics](https://sandbox.zenodo.org/record/1004701)
