import numpy as np


def testGenerator(image):
    image = np.reshape(image, (1, ) + image.shape + (1,))
    yield image


def predict(image, pathToWeights, network):
    model = network()
    model.load_weights(pathToWeights)

    testG = testGenerator(image)
    mask = model.predict_generator(testG, 1, verbose=1)

    return mask
