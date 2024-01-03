import cv2
import numpy as np

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque iaculis laoreet nulla, volutpat blandit mauris dictum quis. Vestibulum eget feugiat mi, sed ultrices nunc. Nullam turpis est, luctus at magna id, ullamcorper fringilla felis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum convallis dapibus lacus, quis lobortis quam consectetur vel. Aenean convallis vitae metus vitae commodo. Praesent id mattis diam. Quisque non neque metus. Vivamus ligula massa, convallis sagittis nibh non, malesuada posuere dolor. Proin auctor auctor justo et sagittis. Aliquam vel varius turpis. Etiam dapibus, urna in vulputate iaculis, urna risus accumsan dolor, quis consectetur lacus diam ut ligula. Integer et maximus lectus. Donec id est sed justo laoreet varius et eget sem. "
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
