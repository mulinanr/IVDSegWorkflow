import os
import pydicom

class WassrCorrector(object):

    def __init__(self, sSlide, hStep, maxOffset, alternating, nDynamics, lmo, gauss, zFilter):
        self.sSlide = sSlide
        self.hStep = hStep
        self.maxOffset = maxOffset
        self.alternating = alternating
        self.nDynamics = nDynamics
        self.lmo = lmo
        self.gauss = gauss
        self.zFilter = zFilter


    def calculateWassrAmlCorrection(self, imageDirectory, mask = None):
        sName = self.defineSName(imageDirectory)
        (rows, columns) = self.getImageSize(imageDirectory)

        if self.alternating:
            Images = loadAndAlternateImages(imageDirectory, self.nDynamics, self.sSlide)
        else:
            Images = loadImages(imageDirectory, self.nDynamics, self.sSlide)


    def defineSName(self, imageDirectory):
        pathArray = os.path.normpath(imageDirectory).lstrip(os.path.sep).split(os.path.sep)
        pathArray[-1] = 'A_' + pathArray[-1]
        sName = os.path.join(*pathArray)
        if not os.path.exists(sName):
            os.makedirs(sName)
        return sName

    def getImageSize(self, imageDirectory):
        filename = os.path.basename(os.path.dirname(imageDirectory)) + '_sl_' + str(self.sSlide) + '_dyn_1'
        dataset = pydicom.dcmread(os.path.join(imageDirectory,filename))
        rows = int(dataset.Rows)
        columns = int(dataset.Columns)
        return (rows, columns)

    def createDefaultMask(self, imageFile, level):
        pass

    def loadImages(self, imageDirectory, nDynamics, sSlide):
        return None

    def loadAndAlternateImages(self, imageDirectory, nDynamics, sSlide):
        return None
    
    def normalizeImages(self, Images):
        return Images

    def applyZFilter(self, Images):
        return Images

    def calculateOffsets(self, maxOffset, Images):
        return (None, None, None)
