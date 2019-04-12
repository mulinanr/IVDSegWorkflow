import pydicom
import os
import numpy
from matplotlib import pyplot, cm
import tifffile as tiff
from PIL.Image import fromarray

PathPng = "../Png/"
PathDicom = "../DICOM/0000DCB6/AA9E9D2B/AAD8F8BA/00003AB1/"

lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if not ".ds_store" in filename.lower() and not ".png" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))

# Get ref file
RefDs = pydicom.read_file(lstFilesDCM[0], force=True)
print(RefDs.items)

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

# The array is sized based on 'ConstPixelDims'
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in lstFilesDCM:

    # read the file
    ds = pydicom.dcmread(filenameDCM)
    if ds.SeriesDescription == 'WASSR':
        name = PathPng + os.path.basename(ds.filename)
        print(name)

        # store the raw image data to files
        #pyplot.imsave(name + '_bw.png', ds.pixel_array, cmap=pyplot.cm.bone)
        #pyplot.imsave(name + '.png', ds.pixel_array)

