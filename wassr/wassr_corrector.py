import numpy as np
import os
import pydicom
import scipy.ndimage
from scipy import signal

from utils import common_functions
from utils import matlab_style_functions


class WassrCorrector(object):

    def __init__(self, sSlide, hStep, maxOffset, alternating, nDynamics, lmo, gauss, zFilter, algoritm):
        self.sSlide = int(sSlide)
        self.hStep = float(hStep)
        self.maxOffset = float(maxOffset)
        self.alternating = common_functions.str2bool(alternating)
        self.nDynamics = int(nDynamics)
        self.lmo = lmo
        self.gauss = float(gauss)
        self.zFilter = common_functions.str2bool(zFilter)
        self.algoritm = algoritm


    def calculateWassrAmlCorrection(self, imageDirectory, sName, filename, Mask):
        if self.alternating:
            (Images, ZeroImage, sequence) = common_functions.loadAndAlternateImages(imageDirectory, filename, self.gauss, self.sSlide, self.nDynamics, Mask)
        else:
            (Images, ZeroImage, sequence) = common_functions.loadImages(imageDirectory, filename, self.gauss, self.sSlide, self.nDynamics, Mask)

        I0 = Images[:, :, 0]
        I1 = Images[:, :, 1]
        I20 = Images[:, :, 20]

        Images = common_functions.normalizeImages(Images, self.nDynamics, Mask)

        if self.zFilter:
            Images = common_functions.applyZFilter(Images)

        (Offset, RootMeasure) = self.calculateOffsets(Images)

        return (Offset, RootMeasure)


    def calculateOffsets(self, Images):
        (rows, columns, pages) = Images.shape

        Offset = np.zeros((rows, columns), dtype = float)
        RootMeasure = np.zeros((rows, columns), dtype = float)

        stepOhneShift = (self.maxOffset * 2) / (self.nDynamics - 2)
        Mppmwerte = np.arange(-self.maxOffset, self.maxOffset, stepOhneShift).transpose()
        Mppmwerte = np.append(Mppmwerte, self.maxOffset)

        for i in range(rows):
            for j in range(columns):
                if Images[i,j,0] != 0:
                    Mintenswerte = Images[i,j,:].squeeze().transpose()
                    (Offset[i, j], RootMeasure[i, j]) = self.algoritm.calculate(Mppmwerte, Mintenswerte)

        return (Offset, RootMeasure)
