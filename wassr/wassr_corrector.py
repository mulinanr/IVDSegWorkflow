import numpy as np
import os
import pydicom
import scipy.ndimage
from scipy import signal

from utils import common_functions
from utils import matlab_style_functions


class WassrCorrector(object):

    def __init__(self, sSlide, hStep, maxOffset, alternating, nDynamics, lmo, gauss, zFilter, algoritm):
        self.sSlide = sSlide
        self.hStep = hStep
        self.maxOffset = maxOffset
        self.alternating = alternating
        self.nDynamics = nDynamics
        self.lmo = lmo
        self.gauss = gauss
        self.zFilter = zFilter
        self.algoritm = algoritm


    def calculateWassrAmlCorrection(self, imageDirectory, sName, filename, Mask = None):

        if Mask.applyZFilter() == None:
            Mask = matlab_style_functions.createDefaultMask(filename + '1', 0.0)

        if self.alternating:
            Images = matlab_style_functions.loadAndAlternateImages(imageDirectory, filename, self.gauss, self.sSlide, self.nDynamics, Mask)
        else:
            Images = matlab_style_functions.loadImages(imageDirectory, filename, self.gauss, self.sSlide, self.nDynamics, Mask)

        Images = self.normalizeImages(Images, Mask)

        if self.zFilter:
            Images = self.applyZFilter(Images)
    
    def normalizeImages(self, Images, Mask):
        np.seterr(divide='ignore', invalid='ignore')
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

    def calculateOffsets(self, Images):
        (rows, columns, pages) = Images.shape

        Offset = np.zeros((rows, columns), dtype = float)
        RootMeasure = np.zeros((rows, columns), dtype = float)
        mppmIntensW = matlab_style_functions.createCellsArray(rows, columns) 
        lowstepIntensW = matlab_style_functions.createCellsArray(rows, columns)

        stepOhneShift = (self.maxOffset * 2) / (self.nDynamics - 2)
        Mppmwerte = np.arange(-self.maxOffset, self.maxOffset, stepOhneShift).transpose()
        Mppmwerte = np.append(Mppmwerte, self.maxOffset)

        for i in range(rows):
            for j in range(columns):
                Mintenswerte = Images[i,j,:].squeeze().transpose()
                (Offset[i, j], RootMeasure[i, j], xData, yData) = self.algoritm.calculate(Mppmwerte, Mintenswerte)
                mppmIntensW[i, j] = [Mppmwerte, Mintenswerte]
                lowstepIntensW[i, j] = [xData, yData]
                pass

        return (Offset, RootMeasure, mppmIntensW, lowstepIntensW)




