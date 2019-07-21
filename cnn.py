#!/usr/bin/env python
# coding: utf-8

import os

import numpy as np
import tensorflow as tf

from keras.utils import to_categorical
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

from PIL import Image

import matplotlib.pyplot as plt
from matplotlib import image

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

#CROP_X =
#960x320+62+0

IMAGE_PATH = os.getcwd() + '/images'
images = []
labels = []

# subfolders of images should be genus names
genera = [folder for folder in os.listdir(IMAGE_PATH)
          if os.path.isdir(os.path.join(IMAGE_PATH, folder))]

if not genera:
    print("Need to download genera first.")
    quit()

for genus in genera:
    new_image_path = os.path.join(IMAGE_PATH, genus)
    for img_file in os.listdir(new_image_path):
        img = Image.open(os.path.join(new_image_path, img_file)).convert('L')
        # crop away the part that all images share
        #img = img.crop((960,320,62,0))

        # shape: (height, width)
        img_array = np.asarray(img)
        img_array = img_array.reshape(img_array.shape[0], img_array.shape[1], 1)

        #plt.imshow(img_array, cmap='gray', vmin=0, vmax=255)
        #plt.show()

        images.append(img_array)

        # parse the species as a label
        labels.append(img_file.split(".")[0].split("-")[1])

#for img in images:
    #print(img)

# one hot encoding on labels
encoder = LabelBinarizer()
one_hot_labels = encoder.fit_transform(labels)

X_train, X_val, y_train, y_val = train_test_split(images, one_hot_labels, test_size=0.2, random_state=31)
X_train = np.array(X_train)
X_val = np.array(X_val)

#X_train_shaped = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
#X_val_shaped = X_val.reshape(X_val.shape[0], X_val.shape[1], X_val.shape[2], 1)

model = Sequential()

model.add(Conv2D(filters=32, input_shape=(X_train.shape[1], X_train.shape[2], 1), data_format="channels_last", kernel_size=2,
                 strides=2, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(4, activation='sigmoid'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10)

#model.predict(test_X_shaped[:4])
