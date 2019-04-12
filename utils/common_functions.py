import numpy as np
import os
import pydicom
import scipy as sc
import scipy.ndimage

from utils import matlab_style_functions


def defineSName(imageDirectory, sSlide):
    pathArray = os.path.normpath(imageDirectory).lstrip(os.path.sep).split(os.path.sep)
    filename = pathArray[-1]
    pathArray[-1] = 'A_' + pathArray[-1]
    sName = os.path.join(*pathArray)

    if not os.path.exists(sName):
        os.makedirs(sName)

    filename = filename + '_sl_' + str(sSlide) + '_dyn_'
    return (sName, filename)

def getImageSize(imageDirectory, sSlide):
    filename = os.path.basename(os.path.dirname(imageDirectory)) + '_sl_' + str(sSlide) + '_dyn_1'
    dataset = pydicom.dcmread(os.path.join(imageDirectory,filename))
    rows = int(dataset.Rows)
    columns = int(dataset.Columns)
    return (rows, columns)

def createDefaultMask(imageFile, level):
    Image = pydicom.dcmread(imageFile).pixel_array
    return np.uint16(Image >= level)


def loadImages(imageDirectory, filename, gauss, sSlide, nDynamics, Mask):
    Filter = matlab_style_functions.matlab_style_gauss2D((gauss, gauss), 1.0)
    (rows, columns) = getImageSize(imageDirectory, sSlide)
    Images = np.empty((rows, columns, nDynamics - 1), dtype=float)
    sequence = np.empty((nDynamics - 1), dtype=int)
    for i in range(2, nDynamics + 1):
        Image = pydicom.dcmread(os.path.join(imageDirectory, filename + str(i))).pixel_array
        if gauss != 0:
            Image = sc.ndimage.correlate(Image.astype(float), Filter, mode='nearest')
        Image = Image * Mask.astype(float)
        Images[:,:,i - 2] = Image
        sequence[i-2] = i

    return (Images, sequence)


def loadAndAlternateImages(imageDirectory, filename, gauss, sSlide, nDynamics, Mask):
    Filter = matlab_style_functions.matlab_style_gauss2D((gauss, gauss), 1.0)
    (rows, columns) = getImageSize(imageDirectory, sSlide)
    Images = np.empty((rows, columns, nDynamics - 1), dtype=float)
    sequence = np.empty((nDynamics - 1), dtype=int)
    counter = 0

    for i in range(2, nDynamics + 1, 2):
        Image = pydicom.dcmread(os.path.join(imageDirectory,filename + str(i))).pixel_array
        if gauss != 0:
            Image = sc.ndimage.correlate(Image.astype(float), Filter, mode='nearest').transpose()
        Image = Image * Mask.astype(float)
        Images[:,:,counter] = Image
        sequence[counter] = i
        counter = counter + 1

    for j in range(nDynamics - 1, 2, -2):
        Image = pydicom.dcmread(os.path.join(imageDirectory,filename + str(j))).pixel_array
        if gauss != 0:
            Image = sc.ndimage.correlate(Image.astype(float), Filter, mode='nearest').transpose()
        Image = Image * Mask.astype(float)
        Images[:,:,counter] = Image
        sequence[counter] = j
        counter = counter + 1           

    return (Images, sequence)

