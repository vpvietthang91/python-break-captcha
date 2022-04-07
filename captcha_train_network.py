import cv2
import glob
import os
import random
import string
import logging
import time

import numpy as np
from tensorflow.keras.optimizers import Adam, SGD
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger
from network_model import NetworkModel

# keep the results reproducible
random.seed(71)

allowed_chars = string.ascii_lowercase + string.digits

def encode(char):
    arr = np.zeros((len(allowed_chars),), dtype="uint8")
    index = allowed_chars.index(char)
    arr[index] = 1
    return arr

def load_dataset(num):
    seg_path = "data/segmented/"

    data = []
    labels = []

    for char in allowed_chars:
        print(f"Loading character data... '{char}'")

        path = seg_path + char + "/"
        files = os.listdir(path)

        for file in files[:num]:
            image = cv2.imread(path + file)
            resized = cv2.resize(image, (30, 30))

            label = encode(char)

            data.append(resized)
            labels.append(label)
    return data, labels

def normalize_samples(data, labels):
    n_data = np.array(data, dtype="float") / 255.0
    n_labels = np.array(labels)
    return n_data, n_labels

def train_network(train_x, train_y, validation_x, validation_y, epochs, learning_rate, batch_size, min_delta, patience, model_name):
    # mod_path to save models
    mod_path = "data/models/" + model_name + "/"

    if not os.path.isdir(mod_path):
        os.makedirs(mod_path)

    sgd = SGD(lr=learning_rate)

    # compile model
    model = NetworkModel.build(30, 30, 3, len(allowed_chars))
    model.compile(loss='categorical_crossentropy', 
                optimizer=sgd, 
                metrics=['accuracy'])

    # data csv
    csv_logger = CSVLogger(mod_path + f'results.csv', separator=";")

    early_stop = EarlyStopping(monitor='val_loss', mode='auto', min_delta=min_delta, patience=patience)

    # train
    model.fit(train_x, train_y, 
                validation_data=(validation_x, validation_y), 
                batch_size=batch_size, 
                epochs=epochs, 
                verbose=1,
                callbacks=[early_stop, csv_logger])

    # save model
    model.save(mod_path + f'model.hdf5')

if __name__ == "__main__":
    num_samples = 2000
    epochs = 1024
    learning_rate = 1e-3
    batch_size = 128
    validation_split=0.66
    min_delta = 1e-6
    patience = 10


    print("Loading dataset...")
    data, labels = load_dataset(num_samples)
    n_data, n_labels = normalize_samples(data, labels)

    print("Separating into training and validation...")
    (train_x, validation_x, train_y, validation_y) = train_test_split(n_data, n_labels, test_size=0.3, random_state=42)

    print("Training network...")
    # nome do arquivo com timestamp    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    model_name = f"model-md[{str(min_delta)}]-pt[{str(patience)}]"
    print(f"Model name: {model_name}")
    
    train_network(train_x, train_y, validation_x, validation_y, epochs, learning_rate, batch_size, min_delta, patience, model_name)

    print("Training completed!")
    print(f"The results were saved in the folder 'data/models/{model_name}'")
