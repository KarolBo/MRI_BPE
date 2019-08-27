import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json, load_model
import glob
import matplotlib.pyplot as plt

class Predictor(object):

    model_1_path = "./model_1/"
    model_2_path = "./model_2/"

    with open(model_1_path+'model.json', 'r') as js_model:
    	model1 = model_from_json(js_model.read())
    model1.load_weights(model_1_path+'model.h5')

    with open(model_2_path+'model.json', 'r') as js_model:
    	model2 = model_from_json(js_model.read())
    model2.load_weights(model_2_path+'model.h5')

    def __init__(self, folder):
        img_rows = 149
        img_cols = 224
        # folder = "/home/mrv6/Desktop/MRI_BPE/cropped_2/1_to_4/Test/"
        datagen = ImageDataGenerator(rescale=1./255)
        self.generator = datagen.flow_from_directory(folder,
                                        target_size=(img_rows, img_cols),
                                        shuffle=False,
                                        class_mode='categorical',
                                        classes=['0', '1', '2', '3'])

    def predict(self):
        prediction1 = self.model1.predict_generator(self.generator)
        prediction1 = np.argmax(prediction1, axis=-1)
        prediction2 = self.model2.predict_generator(self.generator)
        prediction2 = np.argmax(prediction2, axis=-1)
        prediction2[prediction1 == 2] = -1
        return prediction2
