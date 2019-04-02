import os
import shutil
import unittest
from WassrCorrector import WassrCorrector


testFilesPath = '../DICOM_TEST/WASSR_99677/'

sSlide = 1
hStep = 0.01
maxOffset = 1.0
alternating = False
nDynamics = 22
lmo = 'B'
gauss = 3.0
zFilter = False

def createWassrCorrector():
    return WassrCorrector(sSlide, hStep, maxOffset, alternating, nDynamics, lmo, gauss, zFilter)
 

class WassrCorrectorTest(unittest.TestCase):

    def test_constructor(self):
        corrector = createWassrCorrector()

        self.assertEqual(sSlide, corrector.sSlide)
        self.assertEqual(hStep, corrector.hStep)
        self.assertEqual(maxOffset, corrector.maxOffset)
        self.assertEqual(alternating, corrector.alternating)
        self.assertEqual(nDynamics, corrector.nDynamics)
        self.assertEqual(lmo, corrector.lmo)
        self.assertEqual(gauss, corrector.gauss)
        self.assertEqual(zFilter, corrector.zFilter)

    def test_define_save_name(self):
        if os.path.exists('../DICOM_TEST/A_WASSR_99677'):
            shutil.rmtree('../DICOM_TEST/A_WASSR_99677')
        corrector = createWassrCorrector()

        saveName = corrector.defineSName(testFilesPath)

        self.assertEqual(saveName, '../DICOM_TEST/A_WASSR_99677')
        self.assertTrue(os.path.isdir('../DICOM_TEST/A_WASSR_99677'))

    def test_get_image_size(self):
        corrector = createWassrCorrector()
 
        (rows, columns) = corrector.getImageSize(testFilesPath)

        self.assertEqual(rows, 192)
        self.assertEqual(columns, 192)

    def test_create_default_mask(self):
        pass
    
    def test_load_images(self):
        pass
    
    def test_load_and_alternate_images(self):
        pass

    def test_normalize_images(self):
        pass
        
    def test_apply_z_filter(self):
        pass

    def test_calculate_offsets(self):
        pass


if __name__ == '__main__':
    unittest.main()
