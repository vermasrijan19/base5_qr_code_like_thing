import math

import cv2
import numpy as np

decoder= cv2.QRCodeDetector()

def drawFinderPatterns(img, irng,jrng):
    for i in irng:
        for j in jrng:
            i = i - irng[0]
            j=j-jrng[0]
            if (1 <= i <= 5 and 1 <= j <= 5) and (
                    (i >= 1 and (j == 1 or j == 5) or (j >= 1 and (i == 1 or i == 5)))):
                i = i + irng[0]
                j=j+jrng[0]
                img[i][j] = [255, 255, 255]
            else:
                i = i + irng[0]
                j=j+jrng[0]


text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque iaculis laoreet nulla, volutpat blandit "
        "mauris dictum quis. Vestibulum eget feugiat mi, sed ultrices nunc. Nullam turpis est, luctus at magna id, "
        "ullamcorper fringilla felis. Orci varius natoque penatibus et magnis dis parturient montes, "
        "nascetur ridiculus mus. Vestibulum convallis dapibus lacus, quis lobortis quam consectetur vel. Aenean "
        "convallis vitae metus vitae commodo. Praesent id mattis diam. Quisque non neque metus. Vivamus ligula massa, "
        "convallis sagittis nibh non, malesuada posuere dolor. Proin auctor auctor justo et sagittis. Aliquam vel "
        "varius turpis. Etiam dapibus, urna in vulputate iaculis, urna risus accumsan dolor, quis consectetur lacus "
        "diam ut ligula. Integer et maximus lectus. Donec id est sed justo laoreet varius et eget sem.")
# text="1234567890123456"
decimal_text = np.array([ord(c) for c in text])
print(decimal_text)
base5_text = []
for x in decimal_text:
    base5_text.append(np.base_repr(x, base=5))

text = "".join(base5_text)
# print(len(text))
required=math.sqrt(len(text) + 192)
width = math.ceil(required)
height = math.ceil((len(text) + 192)/width)
image = np.zeros([height, width, 3], dtype=np.uint8)
width_counter = 0
height_counter = 0
for x in text:
    while ((width_counter < 8 and height_counter < 8) or (width_counter > width - 9 and height_counter < 8) or
           (width_counter < 8 and height_counter > height - 9)):
        if(width_counter==7 or width_counter==width-8 or height_counter==7 or height_counter==height-8):
            image[height_counter][width_counter] = [255, 255, 255]
        else:
            image[height_counter][width_counter] = [0, 0, 0]
        if width_counter == width - 1:
            width_counter = 0
            height_counter += 1
        else:
            width_counter += 1

    if x == '0':
        image[height_counter][width_counter] = [0, 0, 0]
    elif x == '1':
        image[height_counter][width_counter] = [255, 0, 0]
    elif x == '2':
        image[height_counter][width_counter] = [0, 255, 0]
    elif x == '3':
        image[height_counter][width_counter] = [0, 0, 255]
    elif x == '4':
        image[height_counter][width_counter] = [0, 255, 255]
    if width_counter == width - 1:
        width_counter = 0
        height_counter += 1
    else:
        width_counter += 1
# for i in range(6):
#     for j in range(6):
#         if (i >= 1 and i <= 5 and j >= 1 and j <= 5) and (
#         (i >= 1 and (j == 1 or j == 5) or (j >= 1 and (i == 1 or i == 5)))):
#             image[i][j] = [255, 255, 255]

drawFinderPatterns(image, range(0, 6),range(0, 6))
drawFinderPatterns(image, range(height-7, height),range(0, 6))
drawFinderPatterns(image, range(0,6),range(width-7, width))

image=cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 255,255])
image=cv2.copyMakeBorder(image, 100, 100 ,100, 100, cv2.BORDER_CONSTANT, value=[0, 0,0])

image = np.array(image, dtype=np.uint8)
print(image)
cv2.imwrite("TestEncoding.png", image)  # cv2.waitKey(0)
