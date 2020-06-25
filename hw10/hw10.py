import numpy as np
import cv2
import math

img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
height = img.shape[0]
width = img.shape[1]

border_img = np.zeros((height + 2, width + 2), dtype = np.uint8)
for i in range(height):
    for j in range(width):
        border_img[i + 1, j + 1] = img[i, j]

for i in range(height):
    border_img[i + 1, 0] = img[i, 0]
    border_img[i + 1, width + 1] = img[i, width - 1]

for j in range(width):
    border_img[0, j + 1] = img[0, j]
    border_img[height + 1, j + 1] = img[height - 1, j]

border_img[0, 0] = img[0, 0]
border_img[0, width + 1] = img[0, width - 1]
border_img[height + 1, 0] = img[height - 1, 0]
border_img[height + 1, width + 1] = img[height - 1, width - 1]

border_img_5 = np.zeros((height + 10, width + 10), dtype = np.uint8)
for i in range(height + 10):
    for j in range(width + 10):
        m = i - 5
        n = j - 5
        if (m < 0):
            m = 0
        elif (m >= height):
            m = height - 1
        if (n < 0):
            n = 0
        elif (n >= width):
            n = height - 1
        border_img_5[i, j] = img[m, n]

def Laplace(border_img, threshold):
    lap = np.zeros((height, width), dtype = np.int8)
    mask = np.array([[0, 1, 0],\
                    [1, -4, 1],\
                    [0, 1, 0]])
    for i in range(height):
        for j in range(width):
            val = 0
            for m in range(3):
                for n in range(3):
                    val += mask[m, n] * int(border_img[i + m, j + n])
            if (val >= threshold):
                lap[i, j] = 1
            elif (val <= -1 * threshold):
                lap[i, j] = -1
            else:
                lap[i, j] = 0
    return lap

def Laplace2(border_img, threshold):
    lap2 = np.zeros((height, width), dtype = np.int8)
    mask = np.array([[1, 1, 1],\
                    [1, -8, 1],\
                    [1, 1, 1]])
    for i in range(height):
        for j in range(width):
            val = 0
            for m in range(3):
                for n in range(3):
                    val += mask[m, n] * int(border_img[i + m, j + n])
            if (val >= threshold * 3):
                lap2[i, j] = 1
            elif (val <= threshold * -3):
                lap2[i, j] = -1
            else:
                lap2[i, j] = 0
    return lap2

def minLaplace(border_img, threshold):
    minlap = np.zeros((height, width), dtype = np.int8)
    mask = np.array([[2, -1, 2],\
                    [-1, -4, -1],\
                    [2, -1, 2]])
    for i in range(height):
        for j in range(width):
            val = 0
            for m in range(3):
                for n in range(3):
                    val += mask[m, n] * int(border_img[i + m, j + n])
            if (val >= threshold * 3):
                minlap[i, j] = 1
            elif (val <= threshold * -3):
                minlap[i, j] = -1
            else:
                minlap[i, j] = 0
    return minlap

def LaplacianofGaussian(border_img_5, threshold):
    log = np.zeros((height, width), dtype = np.int8)
    kernel = np.array([	[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],\
				        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],\
				        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],\
				        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],\
				        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],\
				        [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],\
				        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],\
				        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],\
				        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],\
				        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],\
				        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]])
    for i in range(height):
        for j in range(width):
            val = 0
            for m in range(11):
                for n in range(11):
                    val += kernel[n, m] * int(border_img_5[i + m, j + n])
            if (val >= threshold):
                log[i, j] = 1
            elif (val <= threshold * -1):
                log[i, j] = -1
            else:
                log[i, j] = 0
    return log

def DifferenceofGaussian(border_img_5, threshold):
    dog = np.zeros((height, width), dtype = np.int8)
    kernel = np.array([	[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],\
				        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],\
				        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],\
				        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],\
				        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],\
				        [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],\
				        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],\
				        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],\
				        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],\
				        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],\
				        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]])
    for i in range(height):
        for j in range(width):
            val = 0
            for m in range(11):
                for n in range(11):
                    val += kernel[n, m] * int(border_img_5[i + m, j + n])
            if (val >= threshold):
                dog[i, j] = 1
            elif (val <= threshold * -1):
                dog[i, j] = -1
            else:
                dog[i, j] = 0
    return dog

def zero_cross(result, ker_row, ker_col):
    row_size = height + ker_row - 1
    col_size = width + ker_col - 1
    row_frame = ker_row // 2
    col_frame = ker_col // 2
    border_result = np.zeros((row_size, col_size), dtype = np.int8)
    for i in range(row_size):
        for j in range(col_size):
            m = i - row_frame
            n = j - col_frame
            if (m < 0):
                m = 0
            elif (m >= height):
                m = height - 1
            if (n < 0):
                n = 0
            elif (n >= width):
                n = height - 1
            border_result[i, j] = result[m, n]

    edge_img = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width):
            if (result[i, j] == 1):
                cross = 0
                for m in range(ker_row):
                    for n in range(ker_col):
                        if (border_result[i + m, j + n] == -1):
                            cross = 1
                if (cross == 1):
                    edge_img[i, j] = 0
                else:
                    edge_img[i, j] = 255
            else:
                edge_img[i, j] = 255
    return edge_img

laplace = Laplace(border_img, 15)
laplace_img = zero_cross(laplace, 3, 3)
laplace2 = Laplace2(border_img, 15)
laplace2_img = zero_cross(laplace2, 3, 3)
minlaplace = minLaplace(border_img, 20)
minlaplace_img = zero_cross(minlaplace, 3, 3)
lap_gau = LaplacianofGaussian(border_img_5, 3000)
lap_gau_img = zero_cross(lap_gau, 3, 3)
dif_gau = DifferenceofGaussian(border_img_5, 1)
dif_gau_img = zero_cross(dif_gau, 3, 3)

cv2.imwrite('lena_laplace_15.jpeg', laplace_img)
cv2.imwrite('lena_laplace2_15.jpeg', laplace2_img)
cv2.imwrite('lena_min_variance_laplace_20.jpeg', minlaplace_img)
cv2.imwrite('lena_laplacian_of_gaussian_3000.jpeg', lap_gau_img)
cv2.imwrite('lena_difference_of_gaussian_1.jpeg', dif_gau_img)