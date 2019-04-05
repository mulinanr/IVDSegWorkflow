import pydicom
import unittest
import decimal
import scipy

import numpy as np
from scipy import interpolate
from scipy import signal
import scipy.ndimage


filename = '../DICOM_TEST/WASSR_99677/WASSR_99677_sl_1_dyn_1'

def createCellsArray(rows, columns):
    arrayOfCell = np.empty((rows, columns), dtype=object)
    for i in range(len(arrayOfCell)):
        for j in range(len(arrayOfCell[i])):
            arrayOfCell[i][j] = []
    return arrayOfCell

def matlab_style_gauss2D(shape=(3,3), sigma=1.0):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m, n = [(ss-1.)/2. for ss in shape]
    y, x = np.ogrid[-m:m+1, -n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()

    if sumh != 0:
        h /= sumh

    return h

def interpolatePChip1D(x, y, points):
    f = scipy.interpolate.PchipInterpolator(x, y)
    return f(points)

class PythonMethodsTest(unittest.TestCase):

    def test_dicomread(self):
    # Bild1 = dicomread(fullfile(FF,filename1));

        Image = pydicom.dcmread(filename).pixel_array

        self.assertEquals(6, Image[1,1])
        self.assertEquals(7, Image[2,2])
        self.assertEquals(20, Image[70,80])
        self.assertEquals(11, Image[171,177])


    def test_uint16(self):
    # Maske = uint16(Bild1 >= SignalGrenze);
        level = 30 
        Image = pydicom.dcmread(filename).pixel_array

        Mask = np.uint16(Image >= level)

        self.assertEquals(1, Mask[10,96])
        self.assertEquals(1, Mask[66,92])
        self.assertEquals(1, Mask[144,170])
        self.assertEquals(0, Mask[186,176])


    def test_round(self):
    # xsuch = round(x_interp(minind)*100)/100;
        self.assertEquals(-0.5000, round(-0.5000 * 100) / 100)
        self.assertEquals(0.8000, round(0.8001 * 100) / 100)


    def test_abs(self):
    # V_x_interp_mirror_versch = abs(x_interp_mirror_versch - xn);
        float = -54.26
        int = -94

        self.assertEquals(54.26, abs(float))
        self.assertEquals(94, abs(int))


    def test_sum(self):
    # MSCF(1,n_AC) = sum(MSE_Vektor(1,:));
        a = np.array([[1, 4, 7], [2, 5, 8], [3, 6, 9]])

        sum = np.sum(a, axis=0)

        self.assertEquals([6, 15, 24], sum.tolist())


    def test_zeros(self):
    # WASSRBilderalt = zeros(zeilen,spalten,ndyn-1);
        testzeros = np.zeros((192,192), dtype = float)

        self.assertEquals(0.0, testzeros[10,96])
        self.assertEquals(0, testzeros[66,92])
        self.assertEquals(0.0, testzeros[144,170])
        self.assertEquals(0, testzeros[186,176])


    def test_cell(self):
    # MppmIntensW = cell(zeilen,spalten);
        testcells = createCellsArray(192, 192)    
        testvalue = [22, 34.7]

        testcells[5, 7] = testvalue

        self.assertEquals(testvalue, testcells[5, 7])


    def test_multiple_with_dot(self):
    # WASSRBilderalt(:,:,dy) = WASSRBilderalt(:,:,dy).*double(Maske);
        level = 30
        Image = pydicom.dcmread(filename).pixel_array
        Mask = np.uint16(Image >= level)

        result = Image * Mask.astype(float)

        self.assertEquals(30, result[36, 89])
        self.assertEquals(0, result[37, 89])


    def test_squeeze(self):
    # Mintenswerte = squeeze(WASSRBilder(ze,sp,:))'; 
        a = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]])
        sa = a.squeeze()

        self.assertEquals((1, 4, 3), a.shape)
        self.assertEquals((4, 3), sa.shape)


    def test_fspecial(self):
    # myfilter = fspecial('gaussian',[gauss gauss],1.0);
        # G1 = fspecial('gaussian', [3.0 3.0], 1.0)
        G1 = np.array([[0.0751, 0.1238, 0.0751], [0.1238, 0.2042, 0.1238], [0.0751, 0.1238, 0.0751]])
        result1 = matlab_style_gauss2D((3, 3), 1.0)
        # G2 = fspecial('gaussian', [5 1], 1.0)
        G2 = np.array([[0.0545], [0.2442], [0.4026], [0.2442], [0.0545]])
        result2 = matlab_style_gauss2D((5, 1), 1.0)
        self.assertEquals(G1.tolist(), np.around(result1, decimals=4).tolist())
        self.assertEquals(G2.tolist(), np.around(result2, decimals=4).tolist())


    def test_imfilter(self):
    # Bilder(:,:,dy-1) = imfilter(Bilder(:,:,dy-1), myfilter, 'replicate');
        #f = matlab_style_gauss2D((3, 3), 1.0)
        f = np.array([[1, 3], [4, 2]]) 
        a = np.array([[17, 24, 1, 8, 15], 
                     [23, 5, 7, 14, 16],
                     [4, 6, 13, 20, 22], 
                     [10, 12, 19, 21, 3],
                     [11, 18, 25, 2, 9]], dtype = int) 
        b = np.array([[191, 61, 81, 141, 156], 
                     [66, 76, 141, 186, 196],
                     [86, 131, 191, 176, 106], 
                     [126, 191, 186, 56, 66],
                     [145, 215, 135, 55, 90]])
        result = scipy.ndimage.correlate(a.astype(float), f, mode='nearest') #.transpose()
        #result = scipy.ndimage.convolve(a, f, mode='nearest').transpose()
        print(np.around(result, decimals = 4))
        #self.assertEquals(b.tolist(), result.tolist())


    def test_interp1(self):
    # y_interp = interp1(xWerte, yWerte, x_interp, 'pchip');
        x = np.array([1, 2, 3, 4, 5])
        values = np.array([12, 16, 31, 10, 6])
        points = np.array([0, 0.5, 1.5, 5.5, 6])
        expected = np.array([19.3684, 13.6316, 13.2105, 7.4800, 12.5600])
        result = interpolatePChip1D(x, values, points)
        print(result)
        self.assertEquals(expected.tolist(), np.around(result, decimals = 4).tolist())


    def test_filter2(self):
    # my_result2 = filter2(myfilter_Z,y_koor_E);
        a = np.array([[1, 2, 0, 0],[5, 3, 0, 4],[0, 0, 0, 7], [9, 3, 0, 0]])
        k = np.array([[1,1,1],[1,1,0],[1,0,0]])

        result = signal.convolve2d(a, np.rot90(k,2), mode='same')

        self.assertEquals([[1, 8, 5, 0], [8, 11, 5, 4], [8, 17, 10, 11], [9, 12, 10, 7]], result.tolist())


    def test_isnan(self):
    # DD(isnan(DD)) = 0;
        a = np.array([[1, 2, 3], [0, 3, np.NaN]])
        self.assertTrue(np.isnan(a[1, 2]))

        where_are_NaNs = np.isnan(a)
        a[where_are_NaNs] = 0

        self.assertFalse(np.isnan(a[1, 2]))
        self.assertEquals(0, a[1, 2])


    def test_flipud(self):
    # y_koor_E = [flipud(y_koor); y_koor; flipud(y_koor)];
        a = np.array([[1., 0., 0.], [0., 2., 0.], [0., 0., 3.]])

        b = np.flipud(a)

        self.assertEqual([[0., 0., 3.], [0., 2., 0.], [1., 0., 0.]], b.tolist())


if __name__ == '__main__':
    unittest.main()
