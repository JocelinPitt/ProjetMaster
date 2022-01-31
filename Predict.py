import tensorflow.keras as keras
import numpy as np
import pickle
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

EXT = keras.models.load_model("Models/Second_models (Should Works)/model_EXT(5894)")
NEU = keras.models.load_model("Models/Second_models (Should Works)/model_NEU(6194)")
AGR = keras.models.load_model("Models/Second_models (Should Works)/model_AGR(6301)")
CON = keras.models.load_model("Models/Second_models (Should Works)/model_CON(6194)")
OPN = keras.models.load_model("Models/Second_models (Should Works)/model_OPN(6640)")


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

path = r"Models/Second_models (Should Works)/Pickle Datas/psychopath-bert-base-cls-512_head.pkl"
Input, targets = get_inputs('all', path)

'''path_vil = "villain-bert-base-cls-512_head.pkl"
path_her = "hero-bert-base-cls-512_head.pkl"

Input_h, targets_h = get_inputs('all', path_her)
Input_v, targets_v = get_inputs('all', path_vil)'''

EXT_tar = keras.utils.to_categorical(targets[:, 0], num_classes=2)
NEU_tar = keras.utils.to_categorical(targets[:, 1], num_classes=2)
AGR_tar = keras.utils.to_categorical(targets[:, 2], num_classes=2)
CON_tar = keras.utils.to_categorical(targets[:, 3], num_classes=2)
OPN_tar = keras.utils.to_categorical(targets[:, 4], num_classes=2)

EXTscore = EXT.evaluate(Input, EXT_tar, verbose = 0)
NEUscore = NEU.evaluate(Input, NEU_tar, verbose = 0)
ARGscore = AGR.evaluate(Input, AGR_tar, verbose = 0)
CONscore = CON.evaluate(Input, CON_tar, verbose = 0)
OPNscore = OPN.evaluate(Input, OPN_tar, verbose = 0)

EXTpreds = EXT.predict(Input)
NEUpreds = NEU.predict(Input)
AGRpreds = AGR.predict(Input)
CONpreds = CON.predict(Input)
OPNpreds = OPN.predict(Input)

EXTpredsRD = (EXTpreds == EXTpreds.max(axis=1)[:,None]).astype(int)
NEUpredsRD = (NEUpreds == NEUpreds.max(axis=1)[:,None]).astype(int)
AGRpredsRD = (AGRpreds == AGRpreds.max(axis=1)[:,None]).astype(int)
CONpredsRD = (CONpreds == CONpreds.max(axis=1)[:,None]).astype(int)
OPNpredsRD = (OPNpreds == OPNpreds.max(axis=1)[:,None]).astype(int)

print(EXTpredsRD.sum(axis = 0))
print(NEUpredsRD.sum(axis = 0))
print(AGRpredsRD.sum(axis = 0))
print(CONpredsRD.sum(axis = 0))
print(OPNpredsRD.sum(axis = 0))

'''cmEXT = confusion_matrix(targets[:,0].astype(int), EXTpredsRD[:,0])
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
plt.show()'''