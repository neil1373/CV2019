import numpy as np
import cv2

# Preprocessing for getting binary image
original = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
img_height = original.shape[0]
img_width = original.shape[1]

#Setting Kernel
kernel = np.ones((5, 5), dtype = np.uint8)
kernel[4, 4] = kernel[4, 0] = kernel[0, 4] = kernel[0, 0] = 0

def max(kernel, img1, img2):
    for i in range(img_height):
        for j in range(img_width):
            pixel = -1
            for m in range(5):
                for n in range(5):
                    if kernel[m, n] == 1:
                        if (0 <= i + m - 2 < img_height) and (0 <= j + n - 2 < img_width):
                            if img1[i + m - 2, j + n - 2] > pixel:
                                pixel = img1[i + m - 2, j + n - 2]
            img2[i, j] = pixel
    return

def min(kernel, img1, img2):
    for i in range(img_height):
        for j in range(img_width):
            pixel = 256
            for m in range(5):
                for n in range(5):
                    if kernel[m, n] == 1:
                        if (0 <= i + m - 2 < img_height) and (0 <= j + n - 2 < img_width):
                            if img1[i + m - 2, j + n - 2] < pixel:
                                pixel = img1[i + m - 2, j + n - 2]
            img2[i, j] = pixel
    return

# Dilation
dilation = np.zeros((img_height, img_width), dtype = np.uint8)
max(kernel, original, dilation)
cv2.imwrite('lena_gry_dilation.jpeg', dilation)

# Erosion
erosion = np.zeros((img_height, img_width), dtype = np.uint8)
min(kernel, original, erosion)
cv2.imwrite('lena_gry_erosion.jpeg', erosion)

# Opening
opening = np.zeros((img_height, img_width), dtype = np.uint8)
max(kernel, erosion, opening)
cv2.imwrite('lena_gry_opening.jpeg', opening)

# Closing
closing = np.zeros((img_height, img_width), dtype = np.uint8)
min(kernel, dilation, closing)
cv2.imwrite('lena_gry_closing.jpeg', closing)
