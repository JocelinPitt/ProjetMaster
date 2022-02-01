import tensorflow.keras as keras
import numpy as np
import pickle
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

# Import the trained Keras models
EXT = keras.models.load_model("Models/Second_models (Should Works)/model_EXT(5894)")
NEU = keras.models.load_model("Models/Second_models (Should Works)/model_NEU(6194)")
AGR = keras.models.load_model("Models/Second_models (Should Works)/model_AGR(6301)")
CON = keras.models.load_model("Models/Second_models (Should Works)/model_CON(6194)")
OPN = keras.models.load_model("Models/Second_models (Should Works)/model_OPN(6640)")

# This function is taken from Y. Mehta Github. It open a pkl file and prepare it to be transferred to the MLP models.
def get_inputs(layer, path):
    """Read data from pkl file and prepare for training."""
    file = open(
        str(path), "rb"
    )
    data = pickle.load(file)
    author_ids, data_x, data_y = list(zip(*data))
    file.close()

    # alphaW is responsible for which BERT layer embedding we will be using
    if layer == "all":
        alphaW = np.full([12], 1 / 12)

    else:
        alphaW = np.zeros([12])
        alphaW[int(layer) - 1] = 1

    # just changing the way data is stored (tuples of minibatches) and
    # getting the output for the required layer of BERT using alphaW
    inputs = []
    targets = []
    n_batches = len(data_y)
    for ii in range(n_batches):
        inputs.extend(np.einsum("k,kij->ij", alphaW, data_x[ii]))
        targets.extend(data_y[ii])

    inputs = np.array(inputs)
    full_targets = np.array(targets)

    return inputs, full_targets

# This path should be changed to match the pkl file you try to analyse
path = r"Models/Second_models (Should Works)/Pickle Datas/psychopath-bert-base-cls-512_head.pkl"
Input, targets = get_inputs('all', path)

# Those lines transform the 0/1 target value to a 2 column dataframe, those are indicated for the following evaluate
# methode
EXT_tar = keras.utils.to_categorical(targets[:, 0], num_classes=2)
NEU_tar = keras.utils.to_categorical(targets[:, 1], num_classes=2)
AGR_tar = keras.utils.to_categorical(targets[:, 2], num_classes=2)
CON_tar = keras.utils.to_categorical(targets[:, 3], num_classes=2)
OPN_tar = keras.utils.to_categorical(targets[:, 4], num_classes=2)

# Those calculate the evaluate score of the models on the new data we try to analyse
# the output is a 3 values Tuple. [0] = the evaluation on loss, [1] = the evaluation on accuracy
EXTscore = EXT.evaluate(Input, EXT_tar, verbose = 0)
NEUscore = NEU.evaluate(Input, NEU_tar, verbose = 0)
ARGscore = AGR.evaluate(Input, AGR_tar, verbose = 0)
CONscore = CON.evaluate(Input, CON_tar, verbose = 0)
OPNscore = OPN.evaluate(Input, OPN_tar, verbose = 0)

# Those lines try to predict for every row of the Input the presence or absence of a given OCEAN traits
EXTpreds = EXT.predict(Input)
NEUpreds = NEU.predict(Input)
AGRpreds = AGR.predict(Input)
CONpreds = CON.predict(Input)
OPNpreds = OPN.predict(Input)

# Those lines found the maximum value between the presence and absence of a trait and round this one to 1,
# the other one is rounded down to 0
EXTpredsRD = (EXTpreds == EXTpreds.max(axis=1)[:,None]).astype(int)
NEUpredsRD = (NEUpreds == NEUpreds.max(axis=1)[:,None]).astype(int)
AGRpredsRD = (AGRpreds == AGRpreds.max(axis=1)[:,None]).astype(int)
CONpredsRD = (CONpreds == CONpreds.max(axis=1)[:,None]).astype(int)
OPNpredsRD = (OPNpreds == OPNpreds.max(axis=1)[:,None]).astype(int)

# those lines create the confusion matrix between the predicted values and the target values.
cmEXT = confusion_matrix(targets[:,0].astype(int), EXTpredsRD[:,0])
disp1 = ConfusionMatrixDisplay(confusion_matrix=cmEXT, display_labels=['1'])
disp1.plot()
plt.show()

cmNEU = confusion_matrix(targets[:,1].astype(int), NEUpredsRD[:,0])
disp2 = ConfusionMatrixDisplay(confusion_matrix=cmNEU, display_labels=['1'])
disp2.plot()
plt.show()

cmAGR = confusion_matrix(targets[:,2].astype(int), AGRpredsRD[:,0])
disp3 = ConfusionMatrixDisplay(confusion_matrix=cmAGR)
disp3.plot()
plt.show()

cmCON = confusion_matrix(targets[:,3].astype(int), CONpredsRD[:,0])
disp4 = ConfusionMatrixDisplay(confusion_matrix=cmCON)
disp4.plot()
plt.show()

cmOPN = confusion_matrix(OPN_tar[:,1].astype(int), OPNpredsRD[:,0])
disp5 = ConfusionMatrixDisplay(confusion_matrix=cmOPN)
disp5.plot()
plt.show()