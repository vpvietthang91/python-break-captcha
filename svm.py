from __future__ import division
from __future__ import print_function

import os
from os import listdir
from os.path import join, isfile
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import joblib
from prepare_data import process_directory, process_image, image_annotation, crop, adjust, rename, source_from_dir
import glob

chars_list = '0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
chars_dict = {c: chars_list.index(c) for c in chars_list}

def process_data(directory):
    images = []
    labels = []
    image_list = process_directory(directory)
    print("Loading presets....")
    for image_path in image_list:
        #print(image_path)
        images.append(process_image(image_path))
        labels.append(chars_dict[image_path.split('/')[-1].split('-')[0]])
        #labels.append(chars_dict[str(int(image_path.split('/')[-1].split('-')[1].split('.')[0]))])
    return np.array(images), np.array(labels).reshape([len(labels), 1])

def train():
    images, labels = process_data(os.walk("data/chars/"))
    images_train, images_test, labels_train, labels_test = train_test_split(
        images, labels, test_size=0.2, random_state=42)
    print("Training...")
    clf = SVC(kernel="linear", C=10e5)
    # scores = cross_val_score(clf, images, labels, cv = 10)
    # print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    clf.fit(images_train, labels_train)
    print(clf.score(images_test, labels_test))
    joblib.dump(clf, "svm.pkl")
    print("Saved model to svm.pkl")

def predict_char(image_path):
    image = process_image(image_path).reshape(1, -1)
    clf = joblib.load("svm.pkl")
    name = image_path.split('/')[-1].split('-')[0]
    actual = chars_list[clf.predict(image)[0]]
    # print("Predicted: {0}. Actual: {1}".format(name, actual))
    return actual

def predict_string(file_path):
    res = ''
    fileList = source_from_dir(file_path)
    image_annotation(fileList)
    out_path = 'tmp/null/'
    files = glob.glob(out_path+'*')
    for f in files: os.remove(f)
    #crop(file_path, out_path)
    fileList = source_from_dir('data/proceeded_captchas')
    crop(fileList, 'data/crop_captchas')
    adjust('data/crop_captchas')
    #file_list = process_directory(out_path)
    file_list = process_directory('data/crop_captchas')
    for f in sorted(file_list):
        res += predict_char(f)
    print(res)
    return res

if __name__=='__main__':
    if not isfile('svm.pkl'):
        train()
    else:
        #predict_char("")
        predict_string("Capture.jpg")