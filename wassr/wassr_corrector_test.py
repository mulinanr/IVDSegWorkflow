import os
import shutil
import unittest

import numpy as np

from utils import common_functions
from wassr import wassr_corrector
from wassr import algorithm
from wassr import mscf_algorithm


class MockAlgorithm(algorithm.Algorithm):

    def __init__(self, hStep, maxOffset, maxShift):
        self.hStep = hStep
        self.maxOffset = maxOffset
        self.maxShift = maxShift

    def calculate(self, mppmValue, minimalValue):
        return (hStep, maxOffset)


testFilesPath = '../DICOM_TEST/WASSR_99677/'
filename = 'WASSR_99677_sl_1_dyn_'

sSlide = '1'
hStep = '0.01'
maxOffset = '1.0'
alternating = 'False'
nDynamics = '22'
lmo = 'B'
gauss = '3.0'
zFilter = 'False'
algoritm = MockAlgorithm(hStep, maxOffset, maxOffset)

def createWassrCorrector():
    return wassr_corrector.WassrCorrector(sSlide, hStep, maxOffset, alternating, nDynamics, lmo, gauss, zFilter, algoritm)


class WassrCorrectorTest(unittest.TestCase):

    def test_constructor(self):
        corrector = createWassrCorrector()

        self.assertEqual(int(sSlide), corrector.sSlide)
        self.assertEqual(float(hStep), corrector.hStep)
        self.assertEqual(float(maxOffset), corrector.maxOffset)
        self.assertEqual(common_functions.str2bool(alternating), corrector.alternating)
        self.assertEqual(int(nDynamics), corrector.nDynamics)
        self.assertEqual(lmo, corrector.lmo)
        self.assertEqual(float(gauss), corrector.gauss)
        self.assertEqual(common_functions.str2bool(zFilter), corrector.zFilter)


    def test_calculate_wassr_aml_correction(self):
        corrector = createWassrCorrector()
        corrector.algoritm = mscf_algorithm.MscfAlgorithm(hStep, maxOffset, maxOffset)
        sName = '../DICOM_TEST/A_WASSR_99677'        
        Mask = common_functions.createTestMask(192, 192, 5)

        (OF, R) = corrector.calculateWassrAmlCorrection(testFilesPath, sName, filename, Mask)

        self.assertEqual((192, 192), OF.shape)
        self.assertTrue(abs( 0.380000000000000 - OF[0, 0]) < abs(OF[0, 0]) * 0.0001)
        self.assertTrue(abs(-0.190000000000000 - OF[0, 1]) < abs(OF[1, 1]) * 0.0001)
        self.assertTrue(abs( 0.360000000000000 - OF[1, 0]) < abs(OF[1, 0]) * 0.0001)
        self.assertTrue(abs( 0.350000000000000 - OF[1, 1]) < abs(OF[1, 1]) * 0.0001)
        self.assertTrue(abs(-0.600000000000000 - OF[3, 4]) < abs(OF[3, 4]) * 0.0001)
        self.assertTrue(abs( 0.510000000000000 - OF[4, 3]) < abs(OF[4, 3]) * 0.0001)
        self.assertEqual(0.0, OF[5, 5])
        self.assertEqual(0.0, OF[191, 191])

        self.assertEqual((192, 192), R.shape)
        self.assertTrue(abs(1.031706834523456e+02 - R[0, 0]) < abs(R[0, 0]) * 0.0001)
        self.assertTrue(abs(9.948575112426138     - R[0, 1]) < abs(R[1, 1]) * 0.0001)
        self.assertTrue(abs(13.260475788136212    - R[1, 0]) < abs(R[1, 0]) * 0.0001)
        self.assertTrue(abs(6.142879082109577     - R[1, 1]) < abs(R[1, 1]) * 0.0001)
        self.assertTrue(abs(0.786478608844326     - R[3, 4]) < abs(R[3, 4]) * 0.0001)
        self.assertTrue(abs(0.349443498538241     - R[4, 3]) < abs(R[4, 3]) * 0.0001)
        self.assertEqual(0.0, R[5, 5])
        self.assertEqual(0.0, R[191, 191])


    def test_calculate_offsets(self):
        corrector = createWassrCorrector()
        Mask = common_functions.createDefaultMask(os.path.join(testFilesPath, filename + '1'), 0)
        (Images, ZeroImage, sequence) = common_functions.loadImages(testFilesPath, filename, float(gauss), int(sSlide), int(nDynamics), Mask)

        NormalizedImages = common_functions.normalizeImages(Images, int(nDynamics), Mask)

        (result1, result4) = corrector.calculateOffsets(NormalizedImages)

        self.assertEqual((192, 192), result1.shape)
        self.assertEqual((192, 192), result4.shape)

        self.assertEqual(0.01, result1[0, 0])
        self.assertEqual(1.0, result4[0, 0])

