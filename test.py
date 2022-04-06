from tkinter.font import Font
from PIL import ImageFont, ImageDraw, Image
import cv2
import random, string
import numpy as np
import glob

font_path = r'C:\Windows\Fonts'
fonts = glob.glob(font_path+'\\ari*.ttf')
fonts
print(fonts)

# Setting up the canvas
size = random.randint(10,16)
length = random.randint(4,8)
img = np.zeros(((size*2)+5, length*size, 3), np.uint8)
img_pil = Image.fromarray(img+255)

# Drawing text and lines
font = ImageFont.truetype(random.choice(fonts), size)
draw = ImageDraw.Draw(img_pil)
text = ''.join(
    random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) 
               for _ in range(length))
draw.text((5, 10), text, font=font, 
          fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
draw.line([(random.choice(range(length*size)), random.choice(range((size*2)+5)))
           ,(random.choice(range(length*size)), random.choice(range((size*2)+5)))]
          , width=1, fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

# Adding noise and blur
img = np.array(img_pil)
thresh = random.randint(1,5)/100
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        rdn = random.random()
        if rdn < thresh:
            img[i][j] = random.randint(0,123)
        elif rdn > 1-thresh:
            img[i][j] = random.randint(123,255)
img = cv2.blur(img,(int(size/random.randint(5,10)),int(size/random.randint(5,10))))

#Displaying image
cv2.imshow(f"{text}", img)
cv2.waitKey()
cv2.destroyAllWindows()
cv2.imwrite(f"data/{text}.png", img) #if you want to save the image