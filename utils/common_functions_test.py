import numpy as np
import os
import shutil
import unittest

from utils import common_functions


testFilesPath = '../DICOM_TEST/WASSR_99677/'
filename = 'WASSR_99677_sl_1_dyn_'


class CommonFunctionsTest(unittest.TestCase):

    @unittest.skip("We need 'A_' directory for another test data")
    def test_define_save_name(self):
        sSlide = 1
        if os.path.exists('../DICOM_TEST/A_WASSR_99677'):
            shutil.rmtree('../DICOM_TEST/A_WASSR_99677')

        (saveName, filename) =  common_functions.defineSName(testFilesPath, sSlide)

        self.assertEqual(saveName, '../DICOM_TEST/A_WASSR_99677')
        self.assertEqual(filename, 'WASSR_99677_sl_1_dyn_')
        self.assertTrue(os.path.isdir('../DICOM_TEST/A_WASSR_99677'))


    def test_str2bool(self):
        self.assertEqual(True, common_functions.str2bool('true'))
        self.assertEqual(True, common_functions.str2bool('True'))
        self.assertEqual(False, common_functions.str2bool('false'))
        self.assertEqual(False, common_functions.str2bool('False'))
        self.assertEqual(False, common_functions.str2bool('TTrue'))
        self.assertEqual(False, common_functions.str2bool('truee'))
        self.assertEqual(False, common_functions.str2bool(''))

    def test_get_image_size(self):
 
        (rows, columns) = common_functions.getImageSize(testFilesPath, 1)

        self.assertEqual(rows, 192)
        self.assertEqual(columns, 192)

    def test_create_default_mask(self):

        Mask = common_functions.createDefaultMask(os.path.join(testFilesPath, filename + '1'), 0)

        self.assertEqual((192, 192), Mask.shape)
        self.assertEqual('uint16', Mask.dtype)
        
        self.assertEqual(1, Mask[0, 0])
        self.assertEqual(1, Mask[0, 1])
        self.assertEqual(1, Mask[1, 0])
        self.assertEqual(1, Mask[1, 1])
        self.assertEqual(1, Mask[100, 150])
        self.assertEqual(1, Mask[191, 191])

    def test_load_images(self):
        gauss = 0
        sSlide = 1
        nDynamics = 22
        Mask = common_functions.createDefaultMask(os.path.join(testFilesPath, filename + '1'), 0)

        (Images, ZeroImage, sequence) = common_functions.loadImages(testFilesPath, filename, gauss, sSlide, nDynamics, Mask)

        self.assertEqual((192, 192, 21), Images.shape)
        self.assertEqual('float64', Images.dtype)
        self.assertEqual((21, ), sequence.shape)
        self.assertEqual([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], sequence.tolist())
        
        self.assertEqual(0, Images[0, 0, 0])
        self.assertEqual(0, Images[0, 1, 0])
        self.assertEqual(0, Images[1, 0, 0])        
        self.assertEqual(2, Images[1, 1, 0])
        self.assertEqual(11, Images[13, 3, 0])
        self.assertEqual(0, Images[0, 0, 20])
        self.assertEqual(0, Images[0, 1, 20])
        self.assertEqual(0, Images[1, 0, 20])
        self.assertEqual(1, Images[1, 1, 20])
        self.assertEqual(5, Images[13, 3, 20])

    def test_load_images_with_filter(self):
        gauss = 3.0
        sSlide = 1
        nDynamics = 22
        Mask = common_functions.createDefaultMask(os.path.join(testFilesPath, filename + '1'), 0)

        (Images, ZeroImage, sequence) = common_functions.loadImages(testFilesPath, filename, gauss, sSlide, nDynamics, Mask)

        self.assertEqual((192, 192, 21), Images.shape)
        self.assertEqual('float64', Images.dtype)
        self.assertEqual((21, ), sequence.shape)
        self.assertEqual([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], sequence.tolist())

        self.assertTrue(abs(0.150227215908223 - Images[0, 0, 0]) < 0.0001)
        self.assertTrue(abs(0.698364454030617 - Images[0, 1, 0]) < 0.0001)
        self.assertTrue(abs(0.773478061984728 - Images[1, 0, 0]) < 0.0001)
        self.assertTrue(abs(2.31875258394842 - Images[1, 1, 0]) < 0.0001)
        self.assertTrue(abs(5.56523258308949 - Images[13, 3, 0]) < 0.0001)
        self.assertTrue(abs(0.0751136079541115 - Images[0, 0, 20]) < 0.0001 )
        self.assertTrue(abs(0.724750266785866 - Images[0, 1, 20]) < 0.0001 )
        self.assertTrue(abs(0.349182227015308 - Images[1, 0, 20]) < 0.0001 )
        self.assertTrue(abs(1.79177621411671 - Images[1, 1, 20]) < 0.0001 )
        self.assertTrue(abs(4.28333739383741 - Images[13, 3, 20]) < 0.001)

    def test_load_and_alternate_images(self):
        gauss = 0.0
        sSlide = 1
        nDynamics = 22
        Mask = common_functions.createDefaultMask(os.path.join(testFilesPath, filename + '1'), 0)

        (Images, ZeroImage, sequence) = common_functions.loadAndAlternateImages(testFilesPath, filename, gauss, sSlide, nDynamics, Mask)

        self.assertEqual((192, 192, 21), Images.shape)
        self.assertEqual('float64', Images.dtype)
        self.assertEqual((21, ), sequence.shape)
        self.assertEqual([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 21, 19, 17, 15, 13, 11, 9, 7, 5, 3], sequence.tolist())
        
        self.assertEqual(0, Images[0, 0, 0])
        self.assertEqual(0, Images[0, 1, 0])
        self.assertEqual(0, Images[1, 0, 0])
        self.assertEqual(2, Images[1, 1, 0])
        self.assertEqual(11, Images[13, 3, 0])
        self.assertEqual(0, Images[0, 0, 20])
        self.assertEqual(0, Images[0, 1, 20])
        self.assertEqual(0, Images[1, 0, 20])
        self.assertEqual(4, Images[1, 1, 20])
        self.assertEqual(4, Images[13, 3, 20])

    def test_normalize_images(self):
        nDynamics = 22
        Mask = common_functions.createDefaultMask(os.path.join(testFilesPath, filename + '1'), 0)
        (Images, ZeroImage, sequence) = common_functions.loadImages(testFilesPath, filename, 0, 1, nDynamics, Mask)
        Images[1, 2, 3] = np.nan

        self.assertTrue(np.isnan(Images[1, 2, 3]))

        NormalizedImages = common_functions.normalizeImages(Images, nDynamics, Mask)   

        self.assertEqual((192, 192, 21), Images.shape)
        self.assertEqual('float64', Images.dtype)
        self.assertFalse(np.isnan(NormalizedImages[1, 2, 3]))

        self.assertEqual(0, Images[0, 0, 0])
        self.assertEqual(0, Images[0, 1, 0])
        self.assertEqual(0, Images[1, 0, 0])
        self.assertTrue(abs(1.33333333333333 - Images[1, 1, 0]) < 0.0001)
        self.assertEqual(1.375, Images[13, 3, 0])
        self.assertEqual(0, Images[0, 0, 20])
        self.assertEqual(0, Images[0, 1, 20])
        self.assertEqual(0, Images[1, 0, 20])
        self.assertTrue(abs(0.666666666666667 - Images[1, 1, 20]) < 0.0001)
        self.assertEqual(0.625, Images[13, 3, 20])

    def test_apply_z_filter(self):
        #corrector = createWassrCorrector()
        Mask = common_functions.createDefaultMask(os.path.join(testFilesPath, filename + '1'), 0)
        (Images, ZeroImage, sequence) = common_functions.loadImages(testFilesPath, filename, 0, 1, 22, Mask)

        NormalizedImages = common_functions.normalizeImages(Images, 22, Mask)
        FilteredImages = common_functions.applyZFilter(NormalizedImages)

        self.assertEqual((192, 192, 21), FilteredImages.shape)
        self.assertEqual('float64', FilteredImages.dtype)

        self.assertEqual(0, FilteredImages[0, 0, 0])
        self.assertEqual(0, FilteredImages[0, 1, 0])
        self.assertEqual(0, FilteredImages[1, 0, 0])
        self.assertTrue(abs(1.84056407116979 - FilteredImages[1, 1, 0]) < 0.0001)
        self.assertTrue(abs(1.04553537107918 - FilteredImages[13, 3, 0]) < 0.001)
        self.assertEqual(0, FilteredImages[0, 0, 20])
        self.assertEqual(0, FilteredImages[0, 1, 20])
        self.assertEqual(0, FilteredImages[1, 0, 20])
        self.assertTrue(abs(1.62597429880983 - FilteredImages[1, 1, 20]) < 0.0001 )
        self.assertTrue(abs(0.580852661112185 - FilteredImages[13, 3, 20]) < 0.001)

    def test_apply_z_for_filtered_images(self):
        gauss = 3.0
        Mask = common_functions.createDefaultMask(os.path.join(testFilesPath, filename + '1'), 0)
        (Images, ZeroImage, sequence) = common_functions.loadImages(testFilesPath, filename, gauss, 1, 22, Mask)

        NormalizedImages = common_functions.normalizeImages(Images, 22, Mask)
        FilteredImages = common_functions.applyZFilter(NormalizedImages)

        self.assertEqual((192, 192, 21), FilteredImages.shape)
        self.assertEqual('float64', FilteredImages.dtype)

        self.assertTrue(abs(1.84056407116979 - Images[0, 0, 0]) < 0.0001)
        self.assertTrue(abs(1.05657001935004 - Images[0, 1, 0]) < 0.0001)
        self.assertTrue(abs(1.38214242052096 - Images[1, 0, 0]) < 0.0001)
        self.assertTrue(abs(1.11427297830336 - Images[1, 1, 0]) < 0.0001)
        self.assertTrue(abs(1.09200084175353 - Images[13, 3, 0]) < 0.0001)
        self.assertTrue(abs(1.62597429880983 - Images[0, 0, 20]) < 0.0001 )
        self.assertTrue(abs(0.976474890173900 - Images[0, 1, 20]) < 0.0001 )
        self.assertTrue(abs(0.884976279609995 - Images[1, 0, 20]) < 0.0001 )
        self.assertTrue(abs(0.794456714107615 - Images[1, 1, 20]) < 0.0001 )
        self.assertTrue(abs(0.809292561999687 - Images[13, 3, 20]) < 0.001)

