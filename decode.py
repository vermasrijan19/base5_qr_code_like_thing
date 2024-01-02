import cv2
import numpy as np


def base5_to_base10(base5_number):
    base10_number = 0
    power = 0

    # Iterate through each digit in the base-5 number
    for digit in reversed(str(base5_number)):
        # Convert the digit to an integer and add it to the base-10 number
        base10_number += int(digit) * (5 ** power)
        power += 1

    return base10_number


def decode(image):
    text = []
    # print(image/255)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            np.floor_divide(image[i][j], 255, out=image[i][j])
            t = ''.join(map(str, image[i][j]))
            # print(t)
            if t == "001":
                text.append("3")
            elif t == "010":
                text.append("2")
            elif t == "000":
                text.append("0")
            elif t == "111":
                text.append("4")
            elif t == "100":
                text.append("1")
    # combine every 3 elements into 1
    text = [text[i:i + 3] for i in range(0, len(text), 3)]
    final_text = []
    for i in range(len(text)):
        number = int(''.join(text[i]))
        final_text.append(chr(base5_to_base10(number)))
    print("".join(final_text))


def color_threshold(image):
    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define color ranges for each category
    red_lower = np.array([0, 0, 100])
    red_upper = np.array([100, 100, 255])

    blue_lower = np.array([100, 0, 0])
    blue_upper = np.array([255, 100, 100])

    green_lower = np.array([0, 100, 0])
    green_upper = np.array([100, 255, 100])

    white_lower = np.array([200, 200, 200])
    white_upper = np.array([255, 255, 255])

    black_lower = np.array([0, 0, 0])
    black_upper = np.array([50, 50, 50])

    # Create masks for each color range
    red_mask = cv2.inRange(image_rgb, red_lower, red_upper)
    blue_mask = cv2.inRange(image_rgb, blue_lower, blue_upper)
    green_mask = cv2.inRange(image_rgb, green_lower, green_upper)
    white_mask = cv2.inRange(image_rgb, white_lower, white_upper)
    black_mask = cv2.inRange(image_rgb, black_lower, black_upper)

    # Combine the masks
    final_mask = red_mask | blue_mask | green_mask | white_mask | black_mask

    # Apply the mask to the original image
    result = cv2.bitwise_and(image, image, mask=final_mask)

    return result


img = cv2.imread("image.png")
og = img.copy()
# cv2.imshow("og",og)
# print(img)
img = cv2.Canny(img, 100, 200)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones((20, 20), np.uint8))
contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img = cv2.drawContours(img, contours[0], -1, (0, 0, 255), 3)
x, y, w, h = cv2.boundingRect(contours[0][0])
cropped_image = og[y:y + h, x:x + w]

cropped_image = cv2.resize(cropped_image, (33, 76), cv2.INTER_LINEAR)
print(decode(cropped_image))  # cv2.imwrite("img.png",cropped_image)
# cv2.imshow("img",cropped_image)
# cv2.waitKey(0)
