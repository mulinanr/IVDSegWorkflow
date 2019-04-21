import numpy as np

from utils import common_functions
from utils import matlab_style_functions


class CestCorrector(object):

    def __init__(self, sSlide, hStep, maxOffset, abreite, fshift, dfreq, alternating, nDynamics, gauss, S0yn, zFilter):
        self.sSlide = int(sSlide)
        self.hStep = float(hStep)
        self.maxOffset = float(maxOffset)
        self.abreite = float(abreite)
        self.fshift = float(fshift)
        self.dfreq = float(dfreq)
        self.alternating = common_functions.str2bool(alternating)
        self.nDynamics = int(nDynamics)
        self.gauss = float(gauss)
        self.S0yn = int(S0yn)
        self.zFilter = common_functions.str2bool(zFilter)


    def calculateCestAmlEvaluation(self, imageDirectory, Offsets, sName, filename, Mask):
        if self.alternating:
            (Images, ZeroImage, sequence) = common_functions.loadAndAlternateImages(imageDirectory, filename, self.gauss, self.sSlide, self.nDynamics, Mask)
        else:
            (Images, ZeroImage, sequence) = common_functions.loadImages(imageDirectory, filename, self.gauss, self.sSlide, self.nDynamics, Mask)

        if self.zFilter:
            Images = common_functions.applyZFilter(Images)

        (CestCurveS, x_calcentries) = self.calculateCestEvaluation(Images, ZeroImage, Offsets, Mask)

        return (CestCurveS, x_calcentries)


    def calculateCestEvaluation(self, Images, ZeroImage, Offsets, Mask):
        (rows, columns, pages) = Images.shape

        x_calcentries = np.arange(-self.abreite, self.abreite, self.hStep).transpose()
        x_calcentries = np.append(x_calcentries, self.abreite)

        n1 = np.max(x_calcentries)
        n2 = np.argmax(x_calcentries)

        n_calcentries = max(n1, n2)

        CestCurveS = np.zeros((rows, columns, n_calcentries + 1), dtype = float)

        stepOhneShift = (self.maxOffset * 2) / (self.nDynamics - 2)
        deltaH = self.dfreq / 2

        x_1 = np.arange(-self.maxOffset, self.maxOffset, stepOhneShift).transpose()
        x_1 = np.append(x_1, self.maxOffset)

        x_interp = np.arange(-self.maxOffset, self.maxOffset, self.hStep).transpose()
        x_interp = np.append(x_interp, self.maxOffset)

        for i in range(rows):
            for j in range(columns):
                if (Mask[i, j]) != 0:
                    SNull = self.calculateS0yn(i, j, Images, ZeroImage)
                    CestCurveS[i, j, :] = self.calculateCestElement(Images[i, j, :], Offsets[i, j], x_interp, x_1, deltaH, SNull, n_calcentries)
        return (CestCurveS, x_calcentries)


    def calculateS0yn(self, i, j, Images, ZeroImage):
        if self.S0yn == 1:
            SNull = ZeroImage[i, j]
        elif self.S0yn == 0:
            SNull = (Images[i, j, self.nDynamics - 1].squeeze() + Images[i, j, 1].squeeze()) / 2
        elif self.S0yn == 5:
            SNull = Images[1, j, 1].squeeze()
        return SNull
        

    def calculateCestElement(self, Image, offset, x_interp, x_1, deltaH, sNull, n_calcentries):
        vektor = Image.squeeze().transpose()
        y_interp = matlab_style_functions.interpolatePChip1D(x_1, vektor, x_interp)

        if abs(offset) > abs(self.maxOffset - self.abreite):
            offset = 0
        
        vind_sC_1 = abs(x_interp - (-self.abreite + offset))
        vind_sC_2 = abs(x_interp - (self.abreite + offset))
        ind_sC_1 = np.argmin(vind_sC_1)
        ind_sC_2 = np.argmin(vind_sC_2)

        vind_sC_real_1 = abs(x_interp -(-self.abreite))
        vind_sC_real_2 = abs(x_interp -(self.abreite))                
        ind_sC_real_1 = np.argmin(vind_sC_real_1)
        ind_sC_real_2 = np.argmin(vind_sC_real_2)

        y_calcentries = y_interp[ind_sC_1 : ind_sC_2 + 1]

        nycalc2 = len(y_calcentries)
        if nycalc2 == 0:
            y_calcentries = y_interp[ind_sC_real_1 : ind_sC_real_2]

        ycalcentries = y_calcentries[0 : n_calcentries + 1] / float(sNull)

        return ycalcentries[:]

