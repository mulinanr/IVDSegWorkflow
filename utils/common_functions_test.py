import os
import shutil
import unittest
from utils import common_functions



testFilesPath = '../DICOM_TEST/WASSR_99677/'
filename = 'WASSR_99677_sl_1_dyn_'


class CommonFunctionsTest(unittest.TestCase):

    def test_define_save_name(self):
        sSlide = 1
        if os.path.exists('../DICOM_TEST/A_WASSR_99677'):
            shutil.rmtree('../DICOM_TEST/A_WASSR_99677')

        (saveName, filename) =  common_functions.defineSName(testFilesPath, sSlide)

        self.assertEqual(saveName, '../DICOM_TEST/A_WASSR_99677')
        self.assertEqual(filename, 'WASSR_99677_sl_1_dyn_')
        self.assertTrue(os.path.isdir('../DICOM_TEST/A_WASSR_99677'))

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

        (Images, sequence) = common_functions.loadImages(testFilesPath, filename, gauss, sSlide, nDynamics, Mask)

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

        (Images, sequence) = common_functions.loadImages(testFilesPath, filename, gauss, sSlide, nDynamics, Mask)

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

        (Images, sequence) = common_functions.loadAndAlternateImages(testFilesPath, filename, gauss, sSlide, nDynamics, Mask)

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

