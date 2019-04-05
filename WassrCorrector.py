import numpy as np
import os
import pydicom
import scipy.ndimage
from scipy import signal


def matlab_style_gauss2D(shape, sigma=1.0):
    if shape == (0, 0):
        return None

    m, n = [ (ss-1.0) / 2.0 for ss in shape ]
    y, x = np.ogrid[-m : m+1, -n : n+1]
    h = np.exp( -(x * x + y * y) / (2.0 * sigma * sigma) )
    h[ h < np.finfo(h.dtype).eps * h.max() ] = 0
    sumh = h.sum()

    if sumh != 0:
        h /= sumh

    return h


class WassrCorrector(object):

    def __init__(self, sSlide, hStep, maxOffset, alternating, nDynamics, lmo, gauss, zFilter):
        self.sSlide = sSlide
        self.hStep = hStep
        self.maxOffset = maxOffset
        self.alternating = alternating
        self.nDynamics = nDynamics
        self.lmo = lmo
        self.gauss = gauss
        self.zFilter = zFilter


    def calculateWassrAmlCorrection(self, imageDirectory, Mask = None):
        sName = self.defineSName(imageDirectory)
        (rows, columns) = self.getImageSize(imageDirectory)

        if self.alternating:
            Images = loadAndAlternateImages(imageDirectory, self.nDynamics, self.sSlide)
        else:
            Images = loadImages(imageDirectory, self.nDynamics, self.sSlide)


    def defineSName(self, imageDirectory):
        pathArray = os.path.normpath(imageDirectory).lstrip(os.path.sep).split(os.path.sep)
        pathArray[-1] = 'A_' + pathArray[-1]
        sName = os.path.join(*pathArray)
        if not os.path.exists(sName):
            os.makedirs(sName)
        return sName

    def getImageSize(self, imageDirectory):
        filename = os.path.basename(os.path.dirname(imageDirectory)) + '_sl_' + str(self.sSlide) + '_dyn_1'
        dataset = pydicom.dcmread(os.path.join(imageDirectory,filename))
        rows = int(dataset.Rows)
        columns = int(dataset.Columns)
        return (rows, columns)

    def createDefaultMask(self, imageFile, level):
        Image = pydicom.dcmread(imageFile).pixel_array
        return np.uint16(Image >= level)

    def loadImages(self, imageDirectory, filename, Mask):
        Filter = matlab_style_gauss2D((self.gauss, self.gauss), 1.0)
        (rows, columns) = self.getImageSize(imageDirectory)
        Images = np.empty((rows, columns, self.nDynamics - 1), dtype=float)
        sequence = np.empty((self.nDynamics - 1), dtype=int)
        for i in range(2, self.nDynamics + 1):
            Image = pydicom.dcmread(os.path.join(imageDirectory, filename + str(i))).pixel_array
            if self.gauss != 0:
                Image = scipy.ndimage.correlate(Image.astype(float), Filter, mode='nearest')
            Image = Image * Mask.astype(float)
            Images[:,:,i - 2] = Image
            sequence[i-2] = i

        return (Images, sequence)

    def loadAndAlternateImages(self, imageDirectory, filename, Mask):
        Filter = matlab_style_gauss2D((self.gauss, self.gauss), 1.0)
        (rows, columns) = self.getImageSize(imageDirectory)
        Images = np.empty((rows, columns, self.nDynamics - 1), dtype=float)
        sequence = np.empty((self.nDynamics - 1), dtype=int)
        counter = 0

        for i in range(2, self.nDynamics + 1, 2):
            Image = pydicom.dcmread(os.path.join(imageDirectory,filename + str(i))).pixel_array
            if self.gauss != 0:
                Image = scipy.ndimage.correlate(Image.astype(float), Filter, mode='nearest').transpose()
            Image = Image * Mask.astype(float)
            Images[:,:,counter] = Image
            sequence[counter] = i
            counter = counter + 1

        for j in range(self.nDynamics - 1, 2, -2):
            Image = pydicom.dcmread(os.path.join(imageDirectory,filename + str(j))).pixel_array
            if self.gauss != 0:
                Image = scipy.ndimage.correlate(Image.astype(float), Filter, mode='nearest').transpose()
            Image = Image * Mask.astype(float)
            Images[:,:,counter] = Image
            sequence[counter] = j
            counter = counter + 1           

        return (Images, sequence)
    
    def normalizeImages(self, Images, Mask):
        ZeroRemainder =  ( Images[:,:, 0].squeeze() + Images[:, :, self.nDynamics - 2].squeeze() ) / 2

        for i in range(0, self.nDynamics - 1):
            Image = Images[:, :, i]
            Image = Image / ZeroRemainder
            Image = Image * Mask.astype(float)
            elementsNaNs = np.isnan(Image)
            Image[elementsNaNs] = 0
            Images[:, :, i] = Image

        return Images

    def applyZFilter(self, Images):
        Filter = matlab_style_gauss2D((5, 1), 1.0)
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

    def calculateOffsets(self, maxOffset, Images):
        return (None, None, None)
