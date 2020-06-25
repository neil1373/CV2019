import numpy as np
import cv2

# Preprocessing for getting binary image
original = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
img_height = original.shape[0]
img_width = original.shape[1]

#Setting Kernel
kernel = np.ones((5, 5), dtype = np.uint8)
kernel[4, 4] = kernel[4, 0] = kernel[0, 4] = kernel[0, 0] = 0

#Getting Binary Data
binary = np.ones((img_height, img_width), dtype = np.uint8)
for i in range(img_height):
    for j in range(img_width):
        if original[i, j] < 128:
            binary[i, j] = 0
        else:
            binary[i, j] = 255

def union(kernel, img1, img2):
    for i in range(img_height):
        for j in range(img_width):
            pixel = 0
            for m in range(5):
                for n in range(5):
                    if kernel[m, n] == 1:
                        if (0 <= i + m - 2 < img_height) and (0 <= j + n - 2 < img_width):
                            if img1[i + m - 2, j + n - 2] == 255:
                                pixel = 255
            img2[i, j] = pixel
    return

def intersection(kernel, img1, img2):
    for i in range(img_height):
        for j in range(img_width):
            pixel = 255
            for m in range(5):
                for n in range(5):
                    if kernel[m, n] == 1:
                        if (0 <= i + m - 2 < img_height) and (0 <= j + n - 2 < img_width):
                            if img1[i + m - 2, j + n - 2] == 0:
                                pixel = 0
                        else:
                            pixel = 0
            img2[i, j] = pixel
    return

# Dilation
dilation = np.zeros((img_height, img_width), dtype = np.uint8)
union(kernel, binary, dilation)
cv2.imwrite('lena_bin_dilation.jpeg', dilation)

# Erosion
erosion = np.zeros((img_height, img_width), dtype = np.uint8)
intersection(kernel, binary, erosion)
cv2.imwrite('lena_bin_erosion.jpeg', erosion)

# Opening
opening = np.zeros((img_height, img_width), dtype = np.uint8)
union(kernel, erosion, opening)
cv2.imwrite('lena_bin_opening.jpeg', opening)

# Closing
closing = np.zeros((img_height, img_width), dtype = np.uint8)
intersection(kernel, dilation, closing)
cv2.imwrite('lena_bin_closing.jpeg', closing)

# Hit and miss
# L_kernel = np.ones((2, 2), dtype = np.uint8)
# L_kernel[1, 0] = 0
complement = -binary + 255
L_erosion_1 = np.zeros((img_height, img_width), dtype = np.uint8)   # Original erosion
L_erosion_2 = np.zeros((img_height, img_width), dtype = np.uint8)   # Complement erosion
hit_miss = np.zeros((img_height, img_width), dtype = np.uint8)
for i in range(img_height):
    for j in range(img_width):
        if (j - 1 >= 0 and i + 1 < img_height):
            if (binary[i, j - 1] == 255 and binary[i, j] == 255 and binary[i + 1, j] == 255):
                L_erosion_1[i, j] = 255
        if (i - 1 >= 0 and j + 1 < img_width):
            if (complement[i - 1, j] == 255 and complement[i - 1, j + 1] == 255 and complement[i, j + 1] == 255):
                L_erosion_2[i, j] = 255
        if (L_erosion_1[i, j] == L_erosion_2[i, j] == 255):
            hit_miss[i, j] = 255
cv2.imwrite('lena_bin_hit_and_miss.jpeg', hit_miss)