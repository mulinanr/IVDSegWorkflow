import numpy as np

from keras.callbacks import EarlyStopping, ModelCheckpoint
from matplotlib import pyplot

BATCH_SIZE = 40
NUM_EPOCHS = 1
VALIDATION_SPLIT = 0.2


def createPlot(history, weightName):
    pyplot.style.use("ggplot")
    pyplot.figure()
    pyplot.plot(np.arange(0, NUM_EPOCHS), history.history["loss"], label = "train_loss")
    pyplot.plot(np.arange(0, NUM_EPOCHS), history.history["val_loss"], label = "val_loss")
    pyplot.plot(np.arange(0, NUM_EPOCHS), history.history["acc"], label = "train_acc")
    pyplot.plot(np.arange(0, NUM_EPOCHS), history.history["val_acc"], label = "val_acc")
    pyplot.title("Training Loss and Accuracy on Dataset")
    pyplot.xlabel("Epoch #")
    pyplot.ylabel("Loss/Accuracy")
    pyplot.legend(loc = "lower left")
    pyplot.savefig(weightName + ".png")


def train(images, masks, network, weightName):

    early_stopping = EarlyStopping(monitor = 'val_loss', 
                mode = 'min', 
                verbose = 1, 
                patience = 5)
    model_checkpoint = ModelCheckpoint(weightName  + '.hdf5', 
                monitor = 'loss', 
                verbose = 1, 
                save_best_only = True)

    model = network()
    model.summary()

    history = model.fit(images, 
                        masks, 
                        batch_size = BATCH_SIZE, 
                        epochs = NUM_EPOCHS, 
                        verbose = 1, 
                        validation_split = VALIDATION_SPLIT, 
                        shuffle = True, 
                        callbacks = [early_stopping, model_checkpoint])

    createPlot(history, weightName)
