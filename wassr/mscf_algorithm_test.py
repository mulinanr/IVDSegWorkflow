import os
import shutil
import unittest

import numpy as np

from wassr import wassr_corrector
from wassr import mscf_algorithm
from wassr import algorithm


hStep = '0.01'
maxOffset = '1.0'

def createMscfAlgorithm():
    return mscf_algorithm.MscfAlgorithm(hStep, maxOffset, maxOffset)


class MscfAlgorithmTest(unittest.TestCase):

    def test_constructor(self):
        algorithm = createMscfAlgorithm()

        self.assertEqual(float(hStep), algorithm.hStep)
        self.assertEqual(float(maxOffset), algorithm.maxOffset)
        self.assertEqual(float(maxOffset), algorithm.maxShift)


    def test_calculate(self):
        minimalValue = np.array([1.3333, 2.6666, 3.3333, 5.3333, 0.6667, 1.3333, 1.3333, 2.6667, 3.3333, 2.6667, 3.3333, 2.6667, 0.6667, 2.6667, 4, 2.6667, 1.3333, 4.6667,	0, 4, 0.6667])
        mppmValue = np.array([-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        algorithm = createMscfAlgorithm()

        (OF,  R) = algorithm.calculate(mppmValue, minimalValue)
        
        self.assertTrue(abs(0.38 - OF) < OF * 0.0001)
        self.assertTrue(abs(103.170683452346 - R) < R * 0.0001)


    def test_calculate_mscf_aml(self):
        xWerte = np.arange(0.3, 1.01, 0.01).transpose()
        yWerte = np.array([2.66666666666667, 2.83360000000000, 3.01013333333334, 3.18986666666667, 3.36640000000000, 3.53333333333334, 3.68426666666667, 3.81280000000000, 3.91253333333333, 3.97706666666667, 
                            4, 3.97466666666667, 3.90400000000000, 3.79600000000000, 3.65866666666667, 3.50000000000000, 3.32800000000000, 3.15066666666666, 2.97600000000000, 2.81200000000000, 
                            2.66666666666667, 2.52133333333333, 2.35733333333333, 2.18266666666667, 2.00533333333333, 1.83333333333333, 1.67466666666667, 1.53733333333333, 1.42933333333333, 1.35866666666667, 
                            1.33333333333333, 1.42666666666667, 1.68000000000000, 2.05333333333334, 2.50666666666667, 3.00000000000000, 3.49333333333333, 3.94666666666666, 4.32000000000000, 4.57333333333333, 
                            4.66666666666667, 4.53600000000000, 4.18133333333333, 3.65866666666667, 3.02400000000000, 2.33333333333333, 1.64266666666667, 1.00800000000000, 0.485333333333333, 0.130666666666666, 
                            0, 0.112000000000000, 0.416000000000001, 0.863999999999996, 1.40800000000000, 2.00000000000000, 2.59200000000000, 3.13600000000000, 3.58400000000000, 3.88800000000000, 
                            4, 3.96966666666667, 3.87733333333333, 3.72100000000000, 3.49866666666667, 3.20833333333334, 2.84800000000000, 2.41566666666667, 1.90933333333333, 1.32700000000000, 0.666666666666667])

        x_interp_mirror = np.arange(1, -1.01, -0.01).transpose()
        y_interp = np.array([1.33333333333333, 1.49766666666667, 1.65688888888889, 1.81033333333333, 1.95733333333333, 2.09722222222222, 2.22933333333333, 2.35300000000000, 2.46755555555556, 2.57233333333333, 
                            2.66666666666667, 2.74833333333333, 2.81777777777778, 2.87833333333333, 2.93333333333333, 2.98611111111111, 3.04000000000000, 3.09833333333333, 3.16444444444444, 3.24166666666667, 
                            3.33333333333333, 3.47033333333333, 3.66933333333333, 3.91233333333333, 4.18133333333333, 4.45833333333333, 4.72533333333333, 4.96433333333333, 5.15733333333333, 5.28633333333333, 
                            5.33333333333333, 5.20266666666667, 4.84800000000000, 4.32533333333333, 3.69066666666666, 3.00000000000000, 2.30933333333334, 1.67466666666667, 1.15200000000000, 0.797333333333333, 
                            0.666666666666667, 0.685333333333333, 0.735999999999999, 0.810666666666666, 0.901333333333333, 0.999999999999999, 1.09866666666667, 1.18933333333333, 1.26400000000000, 1.31466666666667, 
                            1.33333333333333, 1.33333333333333, 1.33333333333333, 1.33333333333333, 1.33333333333333, 1.33333333333333, 1.33333333333333, 1.33333333333333, 1.33333333333333, 1.33333333333333, 
                            1.33333333333333, 1.36266666666667, 1.44355555555555, 1.56533333333333, 1.71733333333333, 1.88888888888889, 2.06933333333333, 2.24800000000000, 2.41422222222222, 2.55733333333333, 
                            2.66666666666667, 2.75733333333333, 2.84977777777778, 2.94133333333333, 3.02933333333333, 3.11111111111111, 3.18400000000000, 3.24533333333333, 3.29244444444444, 3.32266666666667, 
                            3.33333333333333, 3.31466666666667, 3.26400000000000, 3.18933333333333, 3.09866666666667, 3.00000000000000, 2.90133333333333, 2.81066666666667, 2.73600000000000, 2.68533333333333, 
                            2.66666666666667, 2.68533333333333, 2.73600000000000, 2.81066666666667, 2.90133333333333, 3.00000000000000, 3.09866666666667, 3.18933333333333, 3.26400000000000, 3.31466666666667, 
                            3.33333333333333, 3.32366666666667, 3.29600000000000, 3.25233333333333, 3.19466666666667, 3.12500000000000, 3.04533333333333, 2.95766666666667, 2.86400000000000, 2.76633333333333, 
                            2.66666666666667, 2.52966666666667, 2.33066666666667, 2.08766666666667, 1.81866666666667, 1.54166666666667, 1.27466666666666, 1.03566666666667, 0.842666666666667, 0.713666666666666, 
                            0.666666666666667, 0.708266666666667, 0.823466666666667, 0.997866666666667, 1.21706666666667, 1.46666666666667, 1.73226666666667, 1.99946666666667, 2.25386666666667, 2.48106666666667, 
                            2.66666666666667, 2.83360000000000, 3.01013333333333, 3.18986666666667, 3.36640000000000, 3.53333333333333, 3.68426666666667, 3.81280000000000, 3.91253333333333, 3.97706666666667, 
                            4, 3.97466666666667, 3.90400000000000, 3.79600000000000, 3.65866666666667, 3.50000000000000, 3.32800000000000, 3.15066666666667, 2.97600000000000, 2.81200000000000, 
                            2.66666666666667, 2.52133333333333, 2.35733333333333, 2.18266666666667, 2.00533333333333, 1.83333333333333, 1.67466666666667, 1.53733333333333, 1.42933333333333, 1.35866666666667, 
                            1.33333333333333, 1.42666666666667, 1.68000000000000, 2.05333333333333, 2.50666666666667, 3.00000000000000, 3.49333333333333, 3.94666666666666, 4.32000000000000, 4.57333333333333, 
                            4.66666666666667, 4.53600000000000, 4.18133333333333, 3.65866666666667, 3.02400000000000, 2.33333333333333, 1.64266666666667, 1.00800000000000, 0.485333333333333, 0.130666666666666, 
                            0, 0.112000000000000, 0.416000000000001, 0.863999999999996, 1.40800000000000, 2.00000000000000, 2.59200000000000, 3.13600000000000, 3.58400000000000, 3.88800000000000, 4, 
                            3.96966666666667, 3.87733333333333, 3.72100000000000, 3.49866666666667, 3.20833333333334, 2.84800000000000, 2.41566666666667, 1.90933333333333, 1.32700000000000, 0.666666666666667])
        algorithm = createMscfAlgorithm()

        (OF, R) = algorithm.calculateMscfAml(xWerte, yWerte, x_interp_mirror, y_interp)

        self.assertEqual(0.38, np.around(OF, decimals=2))
        self.assertEqual(103.1707, np.around(R, decimals=4))
