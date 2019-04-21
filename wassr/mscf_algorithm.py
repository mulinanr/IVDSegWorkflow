import numpy as np

from wassr import algorithm
from utils import common_functions
from utils import matlab_style_functions


class MscfAlgorithm(algorithm.Algorithm):

    def __init__(self, hStep, maxOffset, maxShift):
        self.hStep = float(hStep)
        self.maxOffset = float(maxOffset)
        self.maxShift = float(maxShift)


    def calculate(self, mppmValue, minimalValue):
        dppm = 0.5
        OF = 0.0
        wertmin_n = 0.0

        xWerte = mppmValue[:]
        yWerte = minimalValue[:]

        x_start = np.min(xWerte)
        x_end = np.max(xWerte)

        x_interp = np.arange(x_start, x_end, self.hStep).transpose()
        x_interp = np.append(x_interp, x_end)
        x_interp_mirror = -x_interp

        y_interp = matlab_style_functions.interpolatePChip1D(xWerte, yWerte, x_interp)
        minind = np.argmin(y_interp)
        
        xsuch = round(x_interp[minind]  * 100) / 100
        xsuch_minus = xsuch - dppm
        xsuch_plus = xsuch + dppm

        if xsuch_minus <= x_start:
            xsuch_minus = x_start

        if xsuch_plus >= x_end:
            xsuch_plus = x_end

        x_interp_neu = np.arange(xsuch_minus, xsuch_plus, self.hStep).transpose()
        x_interp_neu = np.append(x_interp_neu, xsuch_plus)

        y_interp_neu = matlab_style_functions.interpolatePChip1D(xWerte, yWerte, x_interp_neu)

        (OF, wertmin_n) = self.calculateMscfAml(x_interp_neu, y_interp_neu, x_interp_mirror, y_interp)

        return (OF, wertmin_n)


    def calculateMscfAml(self, xWerte, yWerte, x_interp_mirror, y_interp):
        nPunkte = len(xWerte)
        minind = np.argmin(yWerte)
        xsuch = round( xWerte[minind] * 100) / 100

        start_Abt = xsuch - self.maxShift
        if start_Abt <= -self.maxOffset:
            start_Abt = -self.maxOffset

        ende_Abt = xsuch + self.maxShift 
        if ende_Abt >= self.maxOffset:
            ende_Abt = self.maxOffset

        AbtastvektorC = np.arange(start_Abt, ende_Abt, self.hStep).transpose()
        AbtastvektorC = np.append(AbtastvektorC, ende_Abt)
        siyAC = len(AbtastvektorC)

        MSCF = np.zeros((siyAC), dtype = float)

        for i in range(0, siyAC):
            C = AbtastvektorC[i]
            Xwert_verschobenmirror = np.zeros((nPunkte), dtype = float)
            Ywert_verschobenmirror = np.zeros((nPunkte), dtype = float)

            for j in range(0, nPunkte):
                xn =  xWerte[j]
                x_interp_mirror_versch = x_interp_mirror + 2 * C
                V_x_interp_mirror_versch = abs(x_interp_mirror_versch - xn)
                index = np.argmin(V_x_interp_mirror_versch)
                Xwert_verschobenmirror[j] = x_interp_mirror_versch[index]
                Ywert_verschobenmirror[j] = y_interp[index]

            MSE_Vektor = (Ywert_verschobenmirror - yWerte) * (Ywert_verschobenmirror - yWerte)
            MSCF[i] = MSE_Vektor.sum()

        wertmin = np.min(MSCF)
        indexmin = np.argmin(MSCF)
        C = AbtastvektorC[indexmin]

        return (C, wertmin)
