from sys import argv
from captcha.image import ImageCaptcha
import string, random

import cv2.cv2 as cv
from PIL import Image
from os import listdir
from os.path import join, isfile
from matplotlib import pyplot as plt

def hello_world():
    print("Hello, World!")

def random_string(N):
    return ''.join(random.choice(string.ascii_letters + ' ') for i in range(N))

def random_string_without_spaces(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def generate_catpcha(captcha_amount, captcha_length):
    for amount in range(captcha_amount):
        image = ImageCaptcha(width = 40, height = 90)
        captcha_text = random_string(captcha_length)
        data = image.generate(captcha_text)
        image.write(captcha_text, 'data/captchas/'+random_string_without_spaces(5)+'.png')
    
def source_from_dir(dir):
    print(dir)
    fileList = []
    fileList = [f for f in listdir(dir) if isfile(join(dir, f))]
    print(fileList)
    return fileList

def image_annotation(fileList):
    for captcha in fileList:
        #captchaName = 'captcha/'+captcha
        captchaName = 'data/captchas/'+captcha
        print('Captcha name: '+captchaName)
        src = cv.imread(captchaName, 0)
        img = cv.cvtColor(src, cv.COLOR_GRAY2BGR)
        dst = cv.fastNlMeansDenoisingColored(img, None, 10 ,10 ,7 ,21)
        cv.imwrite('data/test/'+captcha, dst)
        img = Image.open('data/test/'+captcha).convert('P')
        print('Before: ')
        print(img.histogram())
        img = img.point(lambda x: 0 if x<128 else 255, '1')
        print('After: ')
        print(img.histogram())
        img.save('data/test/'+captcha)

def denoising(fileList):
    for captcha in fileList:
        captchaName = 'data/captcha/'+captcha
        print('Captcha name: '+captchaName)
        img = cv.imread('data/captcha/E.png')
        b,g,r = cv.split(img)           # get b,g,r
        rgb_img = cv.merge([r,g,b])     # switch it to rgb

        # Denoising
        dst = cv.fastNlMeansDenoisingColored(img,None,10,10,7,21)

        b,g,r = cv.split(dst)           # get b,g,r
        rgb_dst = cv.merge([r,g,b])     # switch it to rgb

        plt.subplot(211),plt.imshow(rgb_img)
        plt.subplot(212),plt.imshow(rgb_dst)
        plt.show()
        cv.imwrite('data/test/'+captcha, rgb_dst)

def crop(fileList, out_directory):
    #print("Hello, World!")
    for file in fileList:
        proceededCaptchas = 'data/test/'+file
        part = 0
        print(proceededCaptchas)
        img = Image.open(proceededCaptchas)
        print('Croping: '+proceededCaptchas)
        p = img.convert('P')
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

if __name__=='__main__':
    hello_world()
<<<<<<< HEAD
    generate_catpcha(1,1)
=======
    generate_catpcha(100,1)
>>>>>>> cbf7dcbc (rebase)
    fileList = source_from_dir('data/captchas')
    image_annotation(fileList)
    #denoising(fileList)
    fileList = source_from_dir('data/test')
    crop(fileList, 'data/crop_captchas')
    