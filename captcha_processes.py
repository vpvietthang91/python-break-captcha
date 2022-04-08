import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import string

from PIL import Image
from os import listdir, makedirs
from collections import defaultdict
from os.path import join, isdir, splitext

# blur effect 
kernel = (3, 3)
level = 2

# raw captchas
raw_path = "data/raw/"
# segmented captchas
seg_path = "data/segmented/"

allowed_chars = string.ascii_lowercase + string.digits

if not isdir(seg_path):
    makedirs(seg_path)

    for i in allowed_chars:
        makedirs(seg_path + "/" + i)

files = listdir(raw_path)

counts = defaultdict(int)

for file in files:
    print("Processing: "+file)
    image = cv2.imread(raw_path + file, 0)
    letters = splitext(file)[0]

    # blur
    k = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(image,-1,k)

    # threshold
    ret, image = cv2.threshold(dst, 110, 255, cv2.THRESH_BINARY_INV)
    image = cv2.erode(image, kernel, iterations = level)

    connectivity = 4
    output = cv2.connectedComponentsWithStats(image, connectivity, cv2.CV_32S)

    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]

    objects = []

    for i in range(1, num_labels):
        a = stats[i, cv2.CC_STAT_AREA]

        if a > 50:
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]

            objects.append((x, y, w, h))

    objects.sort(key=lambda t: t[0])

    #num_detected = min(len(objects), 4)
    num_detected = min(len(objects), 5)
    for i in range(num_detected):
        o = objects[i]
        x = o[0]
        y = o[1]
        w = o[2]
        h = o[3]

        img = image[y:y+h, x:x+w]
        rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        letter = letters[i]

        filename = "/" + str(counts[letter]).zfill(5) + ".png"

        path = seg_path + letter + "/" + filename
        #path = seg_path + letter + filename
        print("Save crop: "+path)
        cv2.imwrite(path, img)
        counts[letter] += 1