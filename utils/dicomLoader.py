import os
import pydicom
import re
import shutil
import sys


PathDicom = "../DICOM/"
PathResult = "../DICOM_RESULT/"


def extract_series(ds):
    SeriesDescription = re.sub(':', '', ds.SeriesDescription)
    SeriesInstanceUID = ds.SeriesInstanceUID.split('.0.0', 1)[0][-5:]
    return str(SeriesDescription + '_' + SeriesInstanceUID)

def create_directory_list(path):
    lstDirsDCM = []  
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for subdir in subdirList:
            lstDirsDCM.append(os.path.join(dirName,subdir))
    return lstDirsDCM

def rename_dicom_file(ds, oldFilename):
    AcquisitionNumber = 0
    if 'AcquisitionNumber' in ds:
        AcquisitionNumber = ds.AcquisitionNumber
    
    newFilename = os.path.join(PathResult, 
                               extract_series(ds),
                               extract_series(ds) + '_sl_' + 
                               #str(ds.InstanceNumber) + '_dyn_' + 
                               '1' + '_dyn_' + 
                               str(AcquisitionNumber))
    shutil.copyfile(oldFilename, newFilename)

def copy_file(fileDCM):
    try:
        ds = pydicom.dcmread(fileDCM)
        rename_dicom_file(ds, fileDCM)
    except pydicom.errors.InvalidDicomError:
        print('The file ' + fileDCM + ' is not a DICOM file')
        pass
    except IsADirectoryError:
        print('The file ' + fileDCM + ' is a directory')
        pass
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass

def sort_dicom_files(lstDirsDCM):
    for dirnameDCM in lstDirsDCM:
        for fileDCM in os.listdir(dirnameDCM):
            copy_file(os.path.join(dirnameDCM, fileDCM))

def create_series_set(lstDirsDCM):
    seriesSet = set()
    for dirnameDCM in lstDirsDCM:
        for fileDCM in os.listdir(dirnameDCM):
            try:
                ds = pydicom.dcmread(os.path.join(dirnameDCM, fileDCM))
                series = extract_series(ds)
                seriesSet.add(series)
            except:
                #print('The file ' + fileDCM + ' is not a DICOM file')
                #print("Unexpected error:", sys.exc_info()[0])
                pass    
    return seriesSet

def prepare_destinations(seriesSet, path):
    #shutil.rmtree(os.path.join(path), ignore_errors=True)

    if not os.path.isdir(os.path.join(path)):
        os.mkdir(path)

    for serie in seriesSet:
        shutil.rmtree(os.path.join(path, serie), ignore_errors=True)
        os.mkdir(os.path.join(path, serie))

def load_dicom_files():
    print('Sort DICOM files')
    dirList = create_directory_list(PathDicom)
    seriesSet = create_series_set(dirList)
    #print(seriesSet)
    prepare_destinations(seriesSet, PathResult)
    sort_dicom_files(dirList)
    print('Done')

    print(pydicom.dcmread('gagCEST_12_85893_sl_27_dyn_27').items)


if __name__ == "__main__":
    load_dicom_files()
