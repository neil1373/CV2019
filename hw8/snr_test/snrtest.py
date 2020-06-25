import numpy as np
import cv2
import math
import datetime

img1 = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('median_5x5.bmp', cv2.IMREAD_GRAYSCALE)
img3 = cv2.imread('lena_salt_and_pepper_05.jpeg', cv2.IMREAD_GRAYSCALE)
height = img1.shape[0]
width = img1.shape[1]

#Setting Kernel
kernel = np.ones((5, 5), dtype = np.uint8)
kernel[4, 4] = kernel[4, 0] = kernel[0, 4] = kernel[0, 0] = 0

def SNR(img1, img2):
    avg_img1 = 0
    var_img1 = 0
    avg_img2 = 0
    var_img2 = 0
    for i in range(height):
        for j in range(width):
            avg_img1 += img1[i, j]
            if (img2[i, j] >= img1[i, j]):
            	avg_img2 += img2[i, j] - img1[i, j]
            else:
            	avg_img2 -= img1[i, j] - img2[i, j]
    avg_img1 = avg_img1 / (height * width)
    avg_img2 = avg_img2 / (height * width)
    for i in range(height):
        for j in range(width):
            var_img1 += math.pow(img1[i, j] - avg_img1, 2)
            diff = 0
            if (img2[i, j] >= img1[i, j] + avg_img2):
            	diff = img2[i, j] - img1[i, j] - avg_img2
            else:
            	diff = img1[i, j] + avg_img2 - img2[i, j]
            var_img2 += math.pow(diff, 2)
    var_img1 = var_img1 / (height * width)
    var_img2 = var_img2 / (height * width)
    SNRval = math.log(math.sqrt(var_img1) / math.sqrt(var_img2), 10) * 20
    return SNRval

def box_filter(img, size):
    img_box = np.zeros((height, width), dtype = np.uint8)
    center = size // 2
    for i in range(height):
        for j in range(width):
            total, count = 0, 0
            for m in range(size):
                for n in range(size):
                    if ((0 <= (i + m - center) < height) and (0 <= (j + n - center) < width)):
                        total += img[i + m - center, j + n - center]
                        count += 1
            img_box[i, j] = total // count
    return img_box

def median_filter(img, size):
    img_med = np.zeros((height, width), dtype = np.uint8)
    center = size // 2
    for i in range(height):
        for j in range(width):
            pixels = []
            for m in range(size):
                for n in range(size):
                    if ((0 <= (i + m - center) < height) and (0 <= (j + n - center) < width)):
                        pixels.append(img[i + m - center, j + n - center])
            pixels.sort()
            count = len(pixels)
            if (count % 2 == 1):
                img_med[i, j] = pixels[count // 2]
            else:
                tmp = pixels[(count - 1) // 2] / 2 + pixels[count // 2] / 2
                img_med[i, j] = tmp
    return img_med

def max(kernel, img1):
    img2 = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width):
            pixel = -1
            for m in range(5):
                for n in range(5):
                    if kernel[m, n] == 1:
                        if (0 <= i + m - 2 < height) and (0 <= j + n - 2 < width):
                            if img1[i + m - 2, j + n - 2] > pixel:
                                pixel = img1[i + m - 2, j + n - 2]
            img2[i, j] = pixel
    return img2

def min(kernel, img1):
    img2 = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width):
            pixel = 256
            for m in range(5):
                for n in range(5):
                    if kernel[m, n] == 1:
                        if (0 <= i + m - 2 < height) and (0 <= j + n - 2 < width):
                            if img1[i + m - 2, j + n - 2] < pixel:
                                pixel = img1[i + m - 2, j + n - 2]
            img2[i, j] = pixel
    return img2

def opening(kernel, img):
	return max(kernel, min(kernel, img))

def closing(kernel, img):
	return min(kernel, max(kernel, img))

def open_close(kernel, img):
	return closing(kernel, opening(kernel, img))

def close_open(kernel, img):
	return opening(kernel, closing(kernel, img))
	
test1 = open_close(kernel, img3)
test2 = close_open(kernel, img3)
cv2.imwrite('lena_salt_and_pepper_05_open_close.jpeg', test1)
cv2.imwrite('lena_salt_and_pepper_05_close_open.jpeg', test2)
#fp = open("SNRlog.txt", "a")
#fp.write("median 5x5 SNR:" + str(SNR(img1, img2)) + '\n')
#nowtime = datetime.datetime.now()
#fp.write("Log Generated:" + str(nowtime.year) + '/'+ str(nowtime.month) + '/' + str(nowtime.day))
#fp.write(' ' + str(nowtime.hour) + ':' + str(nowtime.minute) + ':' + str(nowtime.second) + '\n' + '\n')
#fp.close()