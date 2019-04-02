import pydicom
import unittest

import numpy as np
from scipy import signal


filename = '../DICOM_TEST/WASSR_99677/WASSR_99677_sl_1_dyn_1'

def createCellsArray(rows, columns):
    arrayOfCell = np.empty((rows, columns),dtype=object)
    for i in range(len(arrayOfCell)):
        for j in range(len(arrayOfCell[i])):
            arrayOfCell[i][j] = []
    return arrayOfCell

class PythonMethodsTest(unittest.TestCase):

# Bild1 = dicomread(fullfile(FF,filename1));
    def test_dicomread(self):

        Image = pydicom.dcmread(filename).pixel_array

        self.assertEquals(6, Image[1,1])
        self.assertEquals(7, Image[2,2])
        self.assertEquals(20, Image[70,80])
        self.assertEquals(11, Image[171,177])

# Maske = uint16(Bild1 >= SignalGrenze);
    def test_uint16(self):
        level = 30
        Image = pydicom.dcmread(filename).pixel_array

        Mask = np.uint16(Image >= level)

        self.assertEquals(1, Mask[10,96])
        self.assertEquals(1, Mask[66,92])
        self.assertEquals(1, Mask[144,170])
        self.assertEquals(0, Mask[186,176])

# WASSRBilderalt = zeros(zeilen,spalten,ndyn-1);
    def test_zeros(self):
        testzeros = np.zeros((192,192), dtype = float)

        self.assertEquals(0.0, testzeros[10,96])
        self.assertEquals(0, testzeros[66,92])
        self.assertEquals(0.0, testzeros[144,170])
        self.assertEquals(0, testzeros[186,176])

# MppmIntensW = cell(zeilen,spalten);
    def test_cell(self):
        testcells = createCellsArray(192, 192)    
        testvalue = [22, 34.7]

        testcells[5, 7] = testvalue

        self.assertEquals(testvalue, testcells[5, 7])

# WASSRBilderalt(:,:,dy) = WASSRBilderalt(:,:,dy).*double(Maske);
    def test_multiple_with_dot(self):
        level = 30
        Image = pydicom.dcmread(filename).pixel_array
        Mask = np.uint16(Image >= level)

        result = Image * Mask.astype(float)

        self.assertEquals(30, result[36, 89])
        self.assertEquals(0, result[37, 89])

# Mintenswerte = squeeze(WASSRBilder(ze,sp,:))'; 
    def test_squeeze(self):
        a = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]])
        sa = a.squeeze()

        self.assertEquals((1, 4, 3), a.shape)
        self.assertEquals((4, 3), sa.shape)

# myfilter = fspecial('gaussian',[gauss gauss],1.0);
    def test_fspecial(self):
        pass

# Bilder(:,:,dy-1) = imfilter(Bilder(:,:,dy-1), myfilter, 'replicate');
    def test_imfilter(self):
        pass

# my_result2 = filter2(myfilter_Z,y_koor_E);
    def test_filter2(self):
        a = np.array([[1, 2, 0, 0],[5, 3, 0, 4],[0, 0, 0, 7], [9, 3, 0, 0]])
        k = np.array([[1,1,1],[1,1,0],[1,0,0]])

        result = signal.convolve2d(a, np.rot90(k,2), mode='same')

        self.assertEquals([[1, 8, 5, 0], [8, 11, 5, 4], [8, 17, 10, 11], [9, 12, 10, 7]], result.tolist())


if __name__ == '__main__':
    unittest.main()
