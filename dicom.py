import pydicom
import os
import numpy
from math import ceil
import subprocess
import scipy.misc

def catch_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Exception in {}: {}".format(func.__name__, e))
    return wrapper

###############################################################################

class MyDicom(object):

    @catch_exceptions
    def __init__(self, path):
        self.path = path
        self.fileList = self.loadData()
        first = pydicom.dcmread(self.fileList[0])
        self.modality = first.Modality
        self.nOfStacks = self.getNumOfStacks(first)
        self.nOfSlices = int(len(self.fileList) / self.nOfStacks)
        self.x = int(first.Rows)
        self.y = int(first.Columns)
        self.pixelSpacing = (float(first.PixelSpacing[0]), float(first.PixelSpacing[1]), float(first.SliceThickness))
        self.dataType = first.pixel_array.dtype
        self.fov = (self.x * self.pixelSpacing[0], self.y * self.pixelSpacing[1])
        self.imagePosition = first.ImagePositionPatient
        try:
            self.sliceSpacing = first.SpacingBetweenSlices
        except:
            self.sliceSpacing = self.pixelSpacing[2]

###############################################################################

    @catch_exceptions
    def loadData(self):
        fileList = []
        allFiles = os.listdir(self.path)
        for filename in allFiles:
            if os.path.isfile(self.path+filename) and \
                (".dcm" in filename.lower() or "." not in filename):
                subprocess.call(("dcmdjpeg", self.path+filename, self.path+filename))
                fileList.append(self.path+filename)
        fileList = sorted(fileList, key=lambda x: pydicom.dcmread(x).InstanceNumber)

        return fileList

###############################################################################

    @catch_exceptions
    def getNumOfStacks(self, someImage):
        sliceDict = dict()
        for n in range(0, len(self.fileList)):
            location = pydicom.dcmread(self.fileList[n]).SliceLocation
            if location in sliceDict:
                sliceDict[location] = sliceDict.get(location) + 1
            else:
                sliceDict[location] = 1
        return list(sliceDict.values())[0]

###############################################################################

    @catch_exceptions
    def getImg(self, z, stack):
        imageNum = stack*self.nOfSlices + z
        ds = pydicom.dcmread(self.fileList[imageNum])
        slice_array = ds.pixel_array
        return slice_array

###############################################################################

    @catch_exceptions
    def report(self):
        print("X dimension: %d"%self.x)
        print("Y dimension: %d"%self.y)
        print("Number of slices: "+str(self.nOfSlices))
        print("Number of stacks: "+str(self.nOfStacks))
        print("Pixel spacing %f, %f, %f"%(self.pixelSpacing[0],
              self.pixelSpacing[1], self.pixelSpacing[2]))
        print("Data type: "+str(self.dataType))
        print("FoV: %f x %f mm"%self.fov)
        print("Image position (upper left corner): %f, %f" \
              %(self.imagePosition[0], self.imagePosition[1]))
        print("Spacing between slices: %f"%self.sliceSpacing)

 ###############################################################################

    @catch_exceptions
    def getStack(self, st=0):
        shape = (self.x, self.y, self.nOfSlices)
        stack = numpy.zeros(shape)
        for z in range(self.nOfSlices):
            stack[:,:,z] = self.getImg(z, st)
        return stack

################################################################################

    @catch_exceptions
    def save_as_jpegs(self, path, st=0):
        for z in range(self.nOfSlices):
            image_array = self.getImg(z, st)
            image_array = numpy.flipud(image_array)
            image_array = self.cut_bottom(image_array)
            scipy.misc.imsave('{}slice_{}.jpg'.format(path, z), image_array)

################################################################################

    def cut_bottom(self, img_np):
        y = img_np.shape[0]
        cut_line = y - y//3 - 1
        return img_np[:cut_line,:]
