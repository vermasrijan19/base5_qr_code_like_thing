import cv2
import numpy as np

text = ("22130140334030004123")
decimal_text = np.array([ord(c) for c in text])
print(decimal_text)
base5_text = []
for x in decimal_text:
    base5_text.append(np.base_repr(x, base=5))

text = "".join(base5_text)
print(len(text))
width = 33
height = int(len(text) / width)+1
image = np.zeros([height, width, 3], dtype=np.uint8)
width_counter = 0
height_counter = 0
for x in text:
    if x == '0':
        image[height_counter][width_counter] = [0, 0, 0]
    elif x == '1':
        image[height_counter][width_counter] = [255, 0, 0]
    elif x == '2':
        image[height_counter][width_counter] = [0, 255, 0]
    elif x == '3':
        image[height_counter][width_counter] = [0, 0, 255]
    elif x == '4':
        image[height_counter][width_counter] = [255, 255, 255]
    if width_counter == width-1:
        width_counter = 0
        height_counter += 1
    else:
        width_counter += 1
image = np.array(image, dtype=np.uint8)
print(image)
cv2.imwrite("EncodingOutput.png", image)  # cv2.waitKey(0)
