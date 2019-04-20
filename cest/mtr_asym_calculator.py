import numpy as np
import math

class MtrAsymCalculator(object):

    def __init__(self, sSlide, fshift, dfreq, lmo, gauss, S0yn, zFilter):
        self.sSlide = sSlide
        self.fshift = fshift
        self.dfreq = dfreq
        self.lmo = lmo
        self.gauss = gauss
        self.S0yn = S0yn
        self.zFilter = zFilter


    def calculateMtrAsymCurves(self, CestCurvesS, x_calcentries, Mask):
        (rows, columns, entries) = CestCurvesS.shape
        entry_mtr = math.ceil(entries / 2)

        MTRasymCurves = np.zeros((rows, columns, 2, entry_mtr), dtype = float)
        MTRasym_Bild = np.zeros((rows, columns), dtype = float)

        for i in range(rows):
            for j in range(columns):
                (MTRasymCurves[i, j, 0, :], MTRasymCurves[i, j, 1, :], MTRasym_Bild[i, j]) = self.calculateMtrAsymElement(CestCurvesS[i, j, 0 : entries], Mask[i, j], entries, x_calcentries)
 
        MTRasym_Bild = MTRasym_Bild / self.dfreq

        return (MTRasymCurves, MTRasym_Bild)


    def calculateMtrAsymElement(self, curves, mask, entries, x_calcentries):
        entry_mtr = math.ceil(entries / 2)
        mtra_erg = np.zeros((entries - entry_mtr + 1, 2), dtype = float)
    

        if mask != 0:
            mtra_erg[:, 0] = x_calcentries[entry_mtr - 1 : entries]
            mtra_rechts = curves[entry_mtr - 1 : entries].squeeze()
            mtra_links  = curves[0 : entry_mtr].squeeze()
            mtra_links = np.flipud(mtra_links)
            mtra_kombi = -mtra_rechts + mtra_links
            mtra_erg[:, 1] = mtra_kombi
        else:
            mtra_erg[:, 0] = x_calcentries[entry_mtr - 1 : entries]
            mtra_erg[:, 1] = np.zeros((len(mtra_erg[:, 1])), dtype = float)

        mtra_erg[:, 1] = mtra_erg[:, 1] * 100

        MTRasymCurves0 = mtra_erg[:, 0].astype('float32').squeeze()
        MTRasymCurves1 = mtra_erg[:, 1].astype('float32').squeeze()

        wert1 = self.fshift - self.dfreq / 2
        wert2 = self.fshift + self.dfreq / 2
        vind1 = abs(mtra_erg[:, 0] - wert1)
        vind2 = abs(mtra_erg[:, 0] - wert2)
        i_1 = np.argmin(vind1)
        i_2 = np.argmin(vind2)

        P_vekt = mtra_erg[i_1 : i_2 + 1, 1]
        hstep = abs(mtra_erg[2, 0] - mtra_erg[1, 0]) 
        s1 = np.sum(P_vekt)
        s2 = np.sum(s1)

        MTRasym_Bild = np.sum(np.sum(P_vekt)) * hstep

        return (MTRasymCurves0, MTRasymCurves1, MTRasym_Bild)


