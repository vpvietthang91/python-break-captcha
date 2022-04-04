import os
from cv2 import imread
import cv2.cv2 as cv
from os import listdir
from os.path import join, isfile
from PIL import Image, ImageChops
import random
import string

import numpy as np

list_chars = [f for f in listdir('data/chars') if isfile(join('data/chars', f)) and 'jpg' in f]

def rand_string(N=6):
    	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def rename(path, filename, letter):
    	os.rename(join(path,filename), join(path, letter+'-' + rand_string() + '.jpg'))

def process_directory(directory):
    file_list = []
    for root, dirs, files, in os.walk("data/chars/"):
        for file in files:
            file_list.append(os.path.join(root,file).replace("\\","/"))
    # for file_name in listdir(directory):
    #     file_path = join(directory, file_name)
    #     if isfile(file_path) and 'jpg' in file_name:
    #         file_list.append(file_path)
    return file_list

def process_image(image_path):
    image = imread(image_path)
    #image = image.reshape(3240,)
    image = image.reshape(49152,)
    return np.array([x/255. for x in image])

def detect_char(path, filename):
    class Fit:
        letter = None
        difference = 0
    best = Fit()
    _img = Image.open(join(path, filename))
    for img_name in list_chars:
        current = Fit()
        img = Image.open(join('data/chars', img_name))
        current.letter = img_name.split('-')[0]
        difference = ImageChops.difference(_img, img)
        for x in range(difference.size[0]):
            for y in range(difference.size[1]):
                current.difference += difference.getpixel((x, y))/255.
        if not best.letter or best.difference > current.difference:
            best = current
    if best.letter == filename.split('-')[0]: return
    print(filename, best.letter)
    rename(path, filename, best.letter)

def hello_world():
    print("Hello, World!")
    
def source_from_dir(dir):
    print(dir)
    fileList = []
    fileList = [f for f in listdir(dir) if isfile(join(dir, f))]
    print(fileList)
    return fileList

def crop(fileList, out_directory):
    #print("Hello, World!")
    for file in fileList:
        proceededCaptchas = 'data/proceeded_captchas/'+file
        part = 0
        print(proceededCaptchas)
        img = Image.open(proceededCaptchas)
        print('Croping: '+proceededCaptchas)
        p = img.convert('L')
        w, h = p.size
        letters = []
        left, right= -1, -1
        found = False
        for i in range(w):
            in_letter = False
            for j in range(h):
                if p.getpixel((i,j)) == 0:
                    in_letter = True
                    break
            if not found and in_letter:
                found = True
                left = i
            if found and not in_letter and i-left > 25:
                found = False
                right = i
                letters.append([left, right])
        origin = proceededCaptchas.split('/')[-1].split('.')[0]
        for [l,r] in letters:
            if r-l < 40:
                bbox = (l, 0, r, h)
                crop = img.crop(bbox)
                crop = crop.resize((30,60))
                crop.save(join(out_directory, '{0:04}_{1}.jpg'.format(part, origin)))
                part += 1
         
def adjust(path):
    cropList = source_from_dir(path)
    for crop in cropList:
        img = Image.open(join(path, crop))
        filePath = join(path, crop)
        p  = img.convert('P')
        w, h = p.size
        start, end = -1, -1
        found = False
        for j in range(h):
            in_letter = False
            for i in range(w):
                if p.getpixel((i,j)) == 0:
                    in_letter = True
                    break
            if not found and in_letter:
                found = True
                start = j
            if found and not in_letter and j-start > 35:
                found = False
                end = j
        bbox = (0, start, w, end)
        crop = img.crop(bbox)
        crop = crop.resize((30,36))
        #crop.save(join(path, crop))
        crop.save(filePath)
 
def image_annotation(fileList):
    for captcha in fileList:
        #captchaName = 'captcha/'+captcha
        captchaName = 'data/temp/'+captcha
        print('Captcha name: '+captchaName)
        src = cv.imread(captchaName, 0)
        img = cv.cvtColor(src, cv.COLOR_GRAY2BGR)
        dst = cv.fastNlMeansDenoisingColored(img, None, 50 ,50 ,7 ,21)
        cv.imwrite('data/proceeded_captchas/'+captcha, dst)
        img = Image.open('data/proceeded_captchas/'+captcha).convert('L')
        img = img.point(lambda x: 0 if x<128 else 255, '1')
        img.save('data/proceeded_captchas/'+captcha)

if __name__=='__main__':
    #hello_world()
    fileList = source_from_dir('data/temp')
    image_annotation(fileList)
    fileList = source_from_dir('data/proceeded_captchas')
    crop(fileList, 'data/crop_captchas')
    adjust('data/crop_captchas')
    pass