import cv2
import numpy as np


def quantize_color(image, target_colors):
    # Convert the image to the RGB color space
    image_rgb = image

    # Reshape the image to a 2D array of pixels
    pixels = image_rgb.reshape((-1, 3))

    # Convert the target colors to a NumPy array
    target_colors = np.array(target_colors)

    # Calculate the Euclidean distance between each pixel and each target color
    distances = np.linalg.norm(pixels[:, np.newaxis, :] - target_colors, axis=2)

    # Find the index of the closest target color for each pixel
    closest_color_indices = np.argmin(distances, axis=1)

    # Assign the closest target color to each pixel
    quantized_pixels = target_colors[closest_color_indices]

    # Reshape the quantized pixels back to the original image shape
    quantized_image = quantized_pixels.reshape(image.shape)

    return quantized_image


image = cv2.imread("plswork.jpg")

aspectRatio = image.shape[1] / float(image.shape[0])
# area=image.shape[1]*image.shape[0]

height = int(np.sqrt(409600 / aspectRatio))
width = int(aspectRatio * height)
image = cv2.resize(image, (width, height))

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
# image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)
img = cv2.Canny(image, 100, 200)

# cropped=image

cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(image, cnts[0], -1, (0,255,0), 3)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    area = cv2.contourArea(c)
    ar = w / float(h)
    if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
        # cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
        ROI = image[y:y + h, x:x + w]
        ROI = cv2.resize(ROI, (54, 54))
        # cv2.imwrite('ROI.png', ROI)
        cropped = ROI

# cropped[:,:,0]=255
hsv=cv2.cvtColor(cropped,cv2.COLOR_BGR2HSV)

hsv[:,:,2]=np.where(hsv[:,:,2]>128,255,0)
# hsv[:,:,1]=np.where(hsv[:,:,1]>128,255,0)
cropped=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

#
# div = 4
# cropped = cropped // div * div + div // 2
cv2.imwrite("cropped.png", cropped)

# cv2.waitKey(0)
