import numpy as np

from keras import backend as K

from model_unet import unet
from model_dilated import dilated_unet
from predict import predict
from train import train


def buildTrainingSet(images, masks):
    imageList = []
    maskList = []
    for x in range(images.shape[0]):
        imageList.append(images[x, :, :])
        maskList.append(masks[x, :, :])
    return (np.array(imageList), np.array(maskList))

def calculateDice(y_pred, y_true):
    y_pred = y_pred[0, :, :, 0]
    intersection = np.sum(y_pred[y_true == 1])
    sum_predict = np.sum(y_pred)
    sum_true = np.sum(y_true)
    dice = (2.0 * intersection) / (sum_predict + sum_true)
    return dice

def tryNetwork(trainImages, trainMasks, evaluateImages, evaluateMasks, network, networkName):
    train(trainImages, trainMasks, network, networkName)
    results = []
    for i in range(evaluateImages.shape[2]):
        predicted = predict(evaluateImages[:, :, i], networkName + '.hdf5', network)
        dice = calculateDice(predicted, evaluateMasks[:, :, i])
        results.append(dice)
    
    for j in range(len(results)):
        print(networkName + ' ' + str(j) + ' ' + str(results[j]))



trainImageFile = 'trainImages.npy'
trainMaskFile = 'trainMasks.npy'
(trainImages, trainMasks) = buildTrainingSet(np.load(trainImageFile), np.load(trainMaskFile))

evaluateImageFile = 'evaluate_images.npy'
evaluateMaskFile = 'evaluate_masks.npy'
evaluateImages = np.load(evaluateImageFile)
evaluateMasks = np.load(evaluateMaskFile)

print('----- ----- ----- ----- ----- -----')
print('unet_04')
tryNetwork(trainImages, trainMasks, evaluateImages, evaluateMasks, unet, "unet_04")
print('----- ----- ----- ----- ----- -----')
print('dilated_05')
tryNetwork(trainImages, trainMasks, evaluateImages, evaluateMasks, dilated_unet, "dilated_05")
print('----- ----- ----- ----- ----- -----')
print('bsunet_04')
#tryNetwork(trainImages, trainMasks, evaluateImages, evaluateMasks, unet, "bsunet_04")
print('----- ----- ----- ----- ----- -----')

