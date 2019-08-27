from dicom import *
import numpy as np
from test import *
from vizualizer import *
from ai_model import *

dc = MyDicom("/home/mrv6/Desktop/MRI_BPE/Application/example_mri/")
dc.report()
# dc.save_as_jpegs("/home/mrv6/Desktop/MRI_BPE/Application/example_mri/jpegs/")
data = dc.getStack()

model = Predictor("/home/mrv6/Desktop/MRI_BPE/Application/example_mri/jpegs/")
prediction = model.predict()
print(prediction)

m = MyDialog()
m.spacing = dc.pixelSpacing
m.data = data
m.categories = prediction
m.display()
m.configure_traits()
