import os
from os.path import join

from tensorflow.keras.models import load_model

import cv2

import numpy as np

from logging_utils import logger

path = os.getcwd()
model = load_model('.//..//dataFiles//cnn_data_model.h5')

def predict_digit(file_name):
    """
    This function gives prediction from
    model for input image
    image: np.array
        image in numpy.ndarray
    prediction:str
        prediction from the model
    """
    try:
        image_path = join(
                          join(
                             path,
                             "input_images"
                             ),
                          file_name
                          )
        img = cv2.imread(image_path,0) 
        image = cv2.resize(img,(28,28))
        img = image.reshape(1,28,28,1)
        img = img/255

        prediction = model.predict(img)
        p = np.argmax(prediction)
        probability = prediction[0][p]
        return p, probability
    except Exception as e:
        logger.error("Something went wrong while extracting "
                    +"faces from mtcnn"
                     + f": {e}", exc_info=True)
        raise e

#print(predict_digit("5.jpg"))
   