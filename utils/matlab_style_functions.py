import numpy as np
import scipy

def matlab_style_gauss2D(shape, sigma=1.0):
    if shape == (0, 0):
        return None

    m, n = [ (ss-1.0) / 2.0 for ss in shape ]
    y, x = np.ogrid[-m : m+1, -n : n+1]
    h = np.exp( -(x * x + y * y) / (2.0 * sigma * sigma) )
    h[ h < np.finfo(h.dtype).eps * h.max() ] = 0
    sumh = h.sum()

    if sumh != 0:
        h /= sumh

    return h

def createCellsArray(rows, columns):
    arrayOfCell = np.empty((rows, columns), dtype=object)
    for i in range(len(arrayOfCell)):
        for j in range(len(arrayOfCell[i])):
            arrayOfCell[i][j] = []
    return arrayOfCell

def interpolatePChip1D(x, y, points):
    f = scipy.interpolate.PchipInterpolator(x, y)
    return f(points)


