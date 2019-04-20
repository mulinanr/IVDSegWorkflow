import numpy as np
import os
import unittest

from cest import cest_corrector
from utils import common_functions
from wassr import wassr_corrector
from wassr import wassr_corrector_test
from wassr import mscf_algorithm_test
from wassr import mscf_algorithm
from wassr import algorithm
from wassr import mscf_algorithm


testFilesPath = '../DICOM_TEST/gagCEST_12_99476/'
filename = 'gagCEST_12_99476_sl_1_dyn_'

sSlide = 1
hStep = 0.01
maxOffset = 4.0
abreite = 3.0
fshift = 1.5
dfreq = 0.6
alternating = False
nDynamics = 32
lmo = 'B'
gauss = 3.0
S0yn = 1
zFilter = False

def createCestCorrector():
    return cest_corrector.CestCorrector(sSlide, hStep, maxOffset, abreite, fshift, dfreq, alternating, nDynamics, lmo, gauss, S0yn, zFilter)

def prepareOfsetts(sName, Mask, hStepA, maxOffsetA):
    wassrFilesPath = '../DICOM_TEST/WASSR_99677/'
    wassrFilename = 'WASSR_99677_sl_1_dyn_'
    wassrCorrector = wassr_corrector_test.createWassrCorrector()
    wassrCorrector.algoritm = mscf_algorithm.MscfAlgorithm(hStepA, maxOffsetA, maxOffsetA)
    (OF, R) = wassrCorrector.calculateWassrAmlCorrection(wassrFilesPath, sName, wassrFilename, Mask)
    return OF


class CestCorrectorTest(unittest.TestCase):

    def test_constructor(self):
        corrector = createCestCorrector()

        self.assertEqual(sSlide, corrector.sSlide)
        self.assertEqual(hStep, corrector.hStep)
        self.assertEqual(maxOffset, corrector.maxOffset)
        self.assertEqual(abreite, corrector.abreite)
        self.assertEqual(fshift, corrector.fshift)
        self.assertEqual(dfreq, corrector.dfreq)
        self.assertEqual(alternating, corrector.alternating)
        self.assertEqual(nDynamics, corrector.nDynamics)
        self.assertEqual(lmo, corrector.lmo)
        self.assertEqual(gauss, corrector.gauss)
        self.assertEqual(S0yn, corrector.S0yn)
        self.assertEqual(zFilter, corrector.zFilter)


    def test_calculateCestAmlEvaluation(self):
        corrector = createCestCorrector()
        sName = '../DICOM_TEST/A_WASSR_99677'
        Mask = common_functions.createTestMask(192, 192, 5)
        Offsets = prepareOfsetts(sName, Mask, 0.01, 1.0)

        (CestCurveS, x_calcentries) = corrector.calculateCestAmlEvaluation(testFilesPath, Offsets, sName, filename, Mask)
        
        self.assertEqual((192, 192, 601), CestCurveS.shape)
        self.assertEqual(np.inf, CestCurveS[0, 0, 0])
        self.assertEqual(1.0150, CestCurveS[5, 5, 0])
        self.assertEqual(1.0313, CestCurveS[5, 5, 1])
        self.assertEqual(1.0455, CestCurveS[5, 5, 2])
        #self.assertTrue(abs(1.0150 -  CestCurveS[4, 4, 0]) < abs(CestCurveS[4, 4, 0]) * 0.0001)
        #self.assertTrue(abs(0 -  CestCurveS[0, 0, 0]) < abs(CestCurveS[0, 0, 0]) * 0.0001)
        #self.assertTrue(abs(0 -  CestCurveS[0, 0, 0]) < abs(CestCurveS[0, 0, 0]) * 0.0001)
        self.assertEqual(0, CestCurveS[191, 191, 0])

        self.assertEqual((601, ), x_calcentries.shape)
        self.assertTrue(abs(-3 -  x_calcentries[0]) < abs(x_calcentries[0]) * 0.0001)
        self.assertTrue(abs(-2 -  x_calcentries[100]) < abs(x_calcentries[0]) * 0.0001)
        self.assertTrue(abs( 3 -  x_calcentries[600]) < abs(x_calcentries[0]) * 0.0001)


    def test_calculate_offsets(self):
        corrector = createCestCorrector()
        Mask = common_functions.createTestMask(192, 192, 4)
        (Images, ZeroImage, sequence) = common_functions.loadImages(testFilesPath, filename, gauss, sSlide, nDynamics, Mask)
        Images = common_functions.normalizeImages(Images, nDynamics, Mask)
        Offsets = np.zeros((192,192), dtype = float)
        
        (cestC, xC) = corrector.calculateCestEvaluation(Images, ZeroImage, Offsets, Mask)

        self.assertEqual((192, 192, 601), cestC.shape)
        self.assertEqual((601,), xC.shape)


    def test_calculateCestElement(self):
        Image = np.array([0.3756, 0.3756, 0.1502, 0.5258, 0.4507, 0.1502, 0.4507, 0.4507, 0.1502, 0.3005, 
                          0.3005, 0.1502, 0.4507, 0.3005, 0.3005, 0.1502, 0.6760, 0.3756, 0.5258, 0.2253, 
                          0.8262, 0.0, 0.1502, 0.5258, 0.0751, 0.3756, 0.3005, 0.0751, 0.3005, 0.3005, 0.3005])
        offset = 0.38
        x_interp = np.arange(-4, 4.01, 0.01).transpose()
        x_1 = np.array([-4, -3.73333333333333, -3.46666666666667, -3.2, -2.93333333333333, 
                        -2.66666666666667, -2.4, -2.13333333333333, -1.86666666666667, 
                        -1.6, -1.33333333333333, -1.06666666666667, -0.8, 
                        -0.533333333333333, -0.266666666666667, 0, 0.266666666666667, 
                        0.533333333333333, 0.8, 1.06666666666667, 1.33333333333333, 1.6, 
                        1.86666666666667, 2.13333333333333, 2.4, 2.66666666666667, 
                        2.93333333333333, 3.2, 3.46666666666667, 3.73333333333333, 4])
        deltaH = 0.3000
        sNull = 2
        n_calcentries = 600
        corrector = createCestCorrector()

        result = corrector.calculateCestElement(Image, offset, x_interp, x_1, deltaH, sNull, n_calcentries)

        self.assertEqual((601,), result.shape)
        self.assertEqual(601, len(result))
        self.assertTrue(abs( 0.087305485445163 - result[0]) < abs(result[0]) * 0.001)
        self.assertTrue(abs( 0.092581629578878 - result[1]) < abs(result[1]) * 0.001)
        self.assertTrue(abs( 0.098586610439772 - result[2]) < abs(result[2]) * 0.001)
        self.assertTrue(abs( 0.149023050880709 - result[100]) < abs(result[100]) * 0.001)
        self.assertTrue(abs( 0.110567230908452 - result[598]) < abs(result[598]) * 0.001)
        self.assertTrue(abs( 0.116544484285160 - result[599]) < abs(result[599]) * 0.001)
        self.assertTrue(abs( 0.122260307096683 - result[600]) < abs(result[600]) * 0.001)

