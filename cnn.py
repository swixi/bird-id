#!/usr/bin/env python
# coding: utf-8

import os

import numpy as np

from keras.utils import to_categorical
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten

from sklearn.model_selection import train_test_split

from PIL import Image

import matplotlib.pyplot as plt
from matplotlib import image

#CROP_X =
#960x320+62+0

image_path = os.getcwd() + '/data/images'
images = []
labels = []

print(os.listdir(image_path))

for img_file in os.listdir(image_path):
    img = Image.open(os.path.join(image_path, img_file)).convert('L')
    #img = img.crop((960,320,62,0))
    img_array = np.asarray(img)

    #plt.imshow(img_array, cmap='gray', vmin=0, vmax=255)
    #plt.show()

    images.append(img_array)
    # Parse the species as a label
    labels.append(img_file.split(".")[0].split("-")[1])

for img in images:
    print(img)

X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.1, random_state=97)



one_hot_train = to_categorical(y_train)
one_hot_val = to_categorical(y_val)
# one_hot_testing = to_categorical(test_y)

X_train_shaped = X_train.reshape(9, X_train[0].shape[0], X_train[0].shape[1], 1)
X_val_shaped = X_val.reshape(1, X_val[0].shape[0], X_val[0].shape[1], 1)
# test_X_shaped = test_X.reshape(10000,28,28,1)

quit()  


model = Sequential()

model.add(Conv2D(filters=32, input_shape=(28,28,1), data_format="channels_last", kernel_size=2, strides=2, activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(1, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

model.fit(X_train_shaped, one_hot_train, validation_data=(X_val_shaped, one_hot_val), epochs=10)

#model.predict(test_X_shaped[:4])
