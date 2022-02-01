# Project Master
This repository is a compilation of scripts that I used during my Master's project.

The goal of those scripts are to perform personality detection on fictional characters.
The personality detection algorithms are made following Y. Mehta procedure [(See Y. Mehta's Github)](https://github.com/yashsmehta/personality-prediction).

In the Archives section, you can find many attempts to conduct personality detection. Those include the works I've done using Google Colabs, but also some tests I made with sentiment analysis
[(See SenticNet web site)](https://www.sentic.net/). In this directory, you can also find many attempts that I've done to build my own Keras models.

The files placed in the root directory and those in the Modified Code directory are the one that I finally used in the final form of my Master's Project.

# How to Use
## SetUp
Clone this repository with:
```bash
git clone git@github.com:JocelinPitt/ProjetMaster.git
```

If you want to create your own models, you should also clone [Y. Mehta GitHub repository ](https://github.com/yashsmehta/personality-prediction)
```bash
git clone git@gitlab.com:ml-automated-personality-detection/personality.git
```

You should also install the required python packages with :
```bash
pip -r requirements.txt
```
Note that not all of those package are needed to perform the last goal of this work. But those will be required if you try to run the archived files.

## Prepare the data
The first thing you must do is download the data file on Zenodo with the links below. In the "Movies speeches by narrative role Dataset", you can find three type of files.
If you download the DATA_full.csv, you will get my raw data. Those data need to be linked with the UCI's cast.html (See below). If you choose to work with those files, you can download
the cast.csv file on Zenodo's "Multiple personality data set". It's the same file that I have edited to be in a CSV format.
With those two file, you can run the Imdb.py file. This operation with try to connect both data frame into a single one.

You can skip this operation as it is a very long process by downloading the Df.pkl, in Zenodo's "Movie speeches by narrative role". This pickled file is a data frame that is the result of the previous operation.
With this file, you can directly call the To_Csv.py script. Or you can also skip this process, and directly download the narrative role csv available on Zenodo (i.e. hero.csv, villain.csv, agent.csv).

Once this is done, and you have your data ready you can clone [Y. Mehta's GitHub repository](https://github.com/yashsmehta/personality-prediction), and substitute some of his python script with the slightly modified one that you'll find in the Modified Code directory.
Then you can follow Y. Metha's process to embed your csv. The modified codes allow you to add a "MyData" argument to the LM_extractor.py calls.

```bash
python LM_extractor.py -dataset_type 'MyData' -token_length 512 -batch_size 32 -embed 'bert-base' -op_dir 'pkl_data'
```

You can also skip this step by downloading my embedded data on Zenodo's "Bert embedded speeches by narrative role".

## Prepare the models
You can either use the pretrained models available on this repository and directly use your embedded data with the Predict.py file.
Or you can train new ones by following Y. Mehta process. If you choose to do so, the MLP_LM_saved.py file allow you to save the models you are training.
To do so you should create a directory called "checkpoint" before following the Y. Mehta procedure.

Train your models on the essays files, which are the Pennebaker et al. / Mairesse et al. golden training files for personality detection, with:
```bash
python LM_extractor.py -dataset_type 'essays' -token_length 512 -batch_size 32 -embed 'bert-base' -op_dir 'pkl_data'
```
Then run MLP_LM_saved.py file to get the saved models in the "checkpoint" directory.

# Python Scripts and data
## Imdb.py
This file goal is to link two dataframe. UCI's cast.html from their Movie Data Set [(See UCI's Machine learning repository web page)](https://archive.ics.uci.edu/ml/datasets/Movie) and 
a Dataframe made by myself in another class work. Those dataframes are to be linked based on their movie title and the fictional character's names, which isn't contained in the UCI dataframe.
To do so, this script has been written using the IMDBpy package.

## Predict.py
This file is a simple script that call trained models to perform personality prediction on the fictional characters both present in the two dataframes previously mentioned.
This script is used to call Keras functions evaluate et predict and produce confusion Matrix. The script include a variable call "path" that should be changed in order to work.

## Replacement.py
This file is a python dictionary that was made to transform my personal dataframe. 
Those transformations are made to help the works of the Imdb.py script. It changes the movies names accordingly to IMDB catalogue.

## To_Csv.py
This file is a simple script that will transform a pandas data frame into a collection of CSVs containing only the Speeches and the OCEAN targets in a y/n format.
This step is required for passing those CSV to Y. Metha's BERT embedding function. This script will produce a CSV for each role present in the main data frame.

## DATAs
Due to file size restriction on Github, no data files were included on this repository. Those can be downloaded on the Zenodo sandbox with the following links:
* [Multiple personality data set](https://sandbox.zenodo.org/record/1004709)
* [Movies speeches by narratives role Dataset](https://sandbox.zenodo.org/record/1004703)
* [Pennebaker et al. // Mairesse et al. // personality dataset, Associated LIWC and Sentics](https://sandbox.zenodo.org/record/1004701)
* [Bert embedded speeches by narrative role](https://sandbox.zenodo.org/record/1005239)
* [UCI's machine learning repository "Movie Data Set"](https://archive.ics.uci.edu/ml/datasets/Movie)