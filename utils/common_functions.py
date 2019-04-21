import numpy as np
import os
import pydicom
import scipy as sc
import scipy.ndimage
from scipy import signal

from utils import matlab_style_functions


def str2bool(value):
    if value.lower() in ("True", "true"):
        return True
    else:
        return False
    

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
    return (int(dataset.Rows), int(dataset.Columns))

def createDefaultMask(imageFile, level):
    Image = pydicom.dcmread(imageFile).pixel_array
    return np.uint16(Image >= level)

def createTestMask(rows, columns, size):
    Mask = np.zeros((rows, columns), dtype = float)
    for i in range (size):
        for j in range (size):
            Mask[i, j] = 1.
    return Mask

def loadImages(imageDirectory, filename, gauss, sSlide, nDynamics, Mask):
    Filter = matlab_style_functions.matlab_style_gauss2D((gauss, gauss), 1.0)
    (rows, columns) = getImageSize(imageDirectory, sSlide)
    Images = np.empty((rows, columns, nDynamics - 1), dtype=float)
    sequence = np.empty((nDynamics - 1), dtype=int)

    ZeroImage = pydicom.dcmread(os.path.join(imageDirectory, filename + '1')).pixel_array
    if gauss != 0:
        ZeroImage = sc.ndimage.correlate(ZeroImage.astype(float), Filter, mode='nearest').astype('uint16')
    ZeroImage = ZeroImage * Mask.astype(float)

    for i in range(2, nDynamics + 1):
        Image = pydicom.dcmread(os.path.join(imageDirectory, filename + str(i))).pixel_array
        if gauss != 0:
            Image = sc.ndimage.correlate(Image.astype(float), Filter, mode='nearest')
        Image = Image * Mask.astype(float)
        Images[:,:,i - 2] = Image
        sequence[i-2] = i

    return (Images, ZeroImage, sequence)

def loadAndAlternateImages(imageDirectory, filename, gauss, sSlide, nDynamics, Mask):
    Filter = matlab_style_functions.matlab_style_gauss2D((gauss, gauss), 1.0)
    (rows, columns) = getImageSize(imageDirectory, sSlide)
    Images = np.empty((rows, columns, nDynamics - 1), dtype=float)
    sequence = np.empty((nDynamics - 1), dtype=int)
    counter = 0

    ZeroImage = pydicom.dcmread(os.path.join(imageDirectory, filename + '1')).pixel_array
    if gauss != 0:
        ZeroImage = sc.ndimage.correlate(ZeroImage.astype(float), Filter, mode='nearest')
    ZeroImage = ZeroImage * Mask.astype(float)

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

    return (Images, ZeroImage, sequence)

def normalizeImages(Images, nDynamics, Mask):
    np.seterr(divide='ignore', invalid='ignore')
    ZeroRemainder =  ( Images[:,:, 0].squeeze() + Images[:, :, nDynamics - 2].squeeze() ) / 2

    for i in range(0, nDynamics - 1):
        Image = Images[:, :, i]
        Image = Image / ZeroRemainder
        Image = Image * Mask.astype(float)
        elementsNaNs = np.isnan(Image)
        Image[elementsNaNs] = 0
        Images[:, :, i] = Image

    return Images

def applyZFilter(Images):
    Filter = matlab_style_functions.matlab_style_gauss2D((5, 1), 1.0)
    (rows, columns, pages) = Images.shape

    for i in range(rows):
        for j in range(columns):
            Pipe = Images[i, j, :].squeeze()
            dim = np.size(Pipe)
            Pipe = np.reshape(Pipe, (dim, 1))

            PipeE = np.concatenate((np.flipud(Pipe), Pipe, np.flipud(Pipe)))
            PipeR = signal.convolve2d(PipeE, np.rot90(Filter,2), mode='same')
            PipeN = PipeR[dim : dim * 2]

            for k in range(dim):
                Images[i, j, k] = PipeN[k, 0]

    return Images

