import numpy as np
import cv2
import random
import math
import datetime

img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
height = img.shape[0]
width = img.shape[1]

#Setting Kernel
kernel = np.ones((5, 5), dtype = np.uint8)
kernel[4, 4] = kernel[4, 0] = kernel[0, 4] = kernel[0, 0] = 0

def gaussian(amplitude):
    gau = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width):
            gau[i, j] = img[i, j] + random.gauss(0, 1) * amplitude
    return gau

def salt_and_pepper(probability):
    sal = np.zeros((height, width), dtype = np.uint8)
    lower, upper = probability, (1 - probability)
    for i in range(height):
       for j in range(width):
           if (random.uniform(0, 1) < lower):
               sal[i, j] = 0
           elif (random.uniform(0, 1) > upper):
               sal[i, j] = 255
           else:
               sal[i, j] = img[i, j]
    return sal

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

fp = open("SNRlog.txt", "a")

#Gaussian 10
gauss_10 = gaussian(10)
cv2.imwrite('lena_gaussian_10.jpeg', gauss_10)
fp.write("gaussian 10 original SNR:" + str(SNR(img, gauss_10)) + '\n')

gauss_10_box_3 = box_filter(gauss_10, 3)
cv2.imwrite('lena_gaussian_10_box_3x3.jpeg', gauss_10_box_3)
fp.write("gaussian 10 3x3 box filter SNR:" + str(SNR(img, gauss_10_box_3)) + '\n')

gauss_10_box_5 = box_filter(gauss_10, 5)
cv2.imwrite('lena_gaussian_10_box_5x5.jpeg', gauss_10_box_5)
fp.write("gaussian 10 5x5 box filter SNR:" + str(SNR(img, gauss_10_box_5)) + '\n')

gauss_10_med_3 = median_filter(gauss_10, 3)
cv2.imwrite('lena_gaussian_10_median_3x3.jpeg', gauss_10_med_3)
fp.write("gaussian 10 3x3 median filter SNR:" + str(SNR(img, gauss_10_med_3)) + '\n')

gauss_10_med_5 = median_filter(gauss_10, 5)
cv2.imwrite('lena_gaussian_10_median_5x5.jpeg', gauss_10_med_5)
fp.write("gaussian 10 5x5 median filter SNR:" + str(SNR(img, gauss_10_med_5)) + '\n')

gauss_10_open_close = open_close(kernel, gauss_10)
cv2.imwrite('lena_gaussian_10_open_close.jpeg', gauss_10_open_close)
fp.write("gaussian 10 opening then closing SNR:" + str(SNR(img, gauss_10_open_close)) + '\n')

gauss_10_close_open = close_open(kernel, gauss_10)
cv2.imwrite('lena_gaussian_10_close_open.jpeg', gauss_10_close_open)
fp.write("gaussian 10 closing then opening SNR:" + str(SNR(img, gauss_10_close_open)) + '\n')

#Gaussian 30
gauss_30 = gaussian(30)
cv2.imwrite('lena_gaussian_30.jpeg', gauss_30)
fp.write("gaussian 30 original SNR:" + str(SNR(img, gauss_30)) + '\n')

gauss_30_box_3 = box_filter(gauss_30, 3)
cv2.imwrite('lena_gaussian_30_box_3x3.jpeg', gauss_30_box_3)
fp.write("gaussian 30 3x3 box filter SNR:" + str(SNR(img, gauss_30_box_3)) + '\n')

gauss_30_box_5 = box_filter(gauss_30, 5)
cv2.imwrite('lena_gaussian_30_box_5x5.jpeg', gauss_30_box_5)
fp.write("gaussian 30 5x5 box filter SNR:" + str(SNR(img, gauss_30_box_5)) + '\n')

gauss_30_med_3 = median_filter(gauss_30, 3)
cv2.imwrite('lena_gaussian_30_median_3x3.jpeg', gauss_30_med_3)
fp.write("gaussian 30 3x3 median filter SNR:" + str(SNR(img, gauss_30_med_3)) + '\n')

gauss_30_med_5 = median_filter(gauss_30, 5)
cv2.imwrite('lena_gaussian_30_median_5x5.jpeg', gauss_30_med_5)
fp.write("gaussian 30 5x5 median filter SNR:" + str(SNR(img, gauss_30_med_5)) + '\n')

gauss_30_open_close = open_close(kernel, gauss_30)
cv2.imwrite('lena_gaussian_30_open_close.jpeg', gauss_30_open_close)
fp.write("gaussian 30 opening then closing SNR:" + str(SNR(img, gauss_30_open_close)) + '\n')

gauss_30_close_open = close_open(kernel, gauss_30)
cv2.imwrite('lena_gaussian_30_close_open.jpeg', gauss_30_close_open)
fp.write("gaussian 30 closing then opening SNR:" + str(SNR(img, gauss_30_close_open)) + '\n')


#Salt and pepper 0.05
salpep_05 = salt_and_pepper(0.05)
cv2.imwrite('lena_salt_and_pepper_05.jpeg', salpep_05)
fp.write("salt and pepper 0.05 original SNR:" + str(SNR(img, salpep_05)) + '\n')

salpep_05_box_3 = box_filter(salpep_05, 3)
cv2.imwrite('lena_salt_and_pepper_05_box_3x3.jpeg', salpep_05_box_3)
fp.write("salt and pepper 0.05 3x3 box filter SNR:" + str(SNR(img, salpep_05_box_3)) + '\n')

salpep_05_box_5 = box_filter(salpep_05, 5)
cv2.imwrite('lena_salt_and_pepper_05_box_5x5.jpeg', salpep_05_box_5)
fp.write("salt and pepper 0.05 5x5 box filter SNR:" + str(SNR(img, salpep_05_box_5)) + '\n')

salpep_05_med_3 = median_filter(salpep_05, 3)
cv2.imwrite('lena_salt_and_pepper_05_median_3x3.jpeg', salpep_05_med_3)
fp.write("salt and pepper 0.05 3x3 median filter SNR:" + str(SNR(img, salpep_05_med_3)) + '\n')

salpep_05_med_5 = median_filter(salpep_05, 5)
cv2.imwrite('lena_salt_and_pepper_05_median_5x5.jpeg', salpep_05_med_5)
fp.write("salt and pepper 0.05 5x5 median filter SNR:" + str(SNR(img, salpep_05_med_5)) + '\n')

salpep_05_open_close = open_close(kernel, salpep_05)
cv2.imwrite('lena_salt_and_pepper_05_open_close.jpeg', salpep_05_open_close)
fp.write("salt and pepper 0.05 opening then closing SNR:" + str(SNR(img, salpep_05_open_close)) + '\n')

salpep_05_close_open = close_open(kernel, salpep_05)
cv2.imwrite('lena_salt_and_pepper_05_close_open.jpeg', salpep_05_close_open)
fp.write("salt and pepper 0.05 closing then opening SNR:" + str(SNR(img, salpep_05_close_open)) + '\n')

#Salt and pepper 0.1
salpep_10 = salt_and_pepper(0.1)
cv2.imwrite('lena_salt_and_pepper_10.jpeg', salpep_10)
fp.write("salt and pepper 0.1 original SNR:" + str(SNR(img, salpep_10)) + '\n')

salpep_10_box_3 = box_filter(salpep_10, 3)
cv2.imwrite('lena_salt_and_pepper_10_box_3x3.jpeg', salpep_10_box_3)
fp.write("salt and pepper 0.1 3x3 box filter SNR:" + str(SNR(img, salpep_10_box_3)) + '\n')

salpep_10_box_5 = box_filter(salpep_10, 5)
cv2.imwrite('lena_salt_and_pepper_10_box_5x5.jpeg', salpep_10_box_5)
fp.write("salt and pepper 0.1 5x5 box filter SNR:" + str(SNR(img, salpep_10_box_5)) + '\n')

salpep_10_med_3 = median_filter(salpep_10, 3)
cv2.imwrite('lena_salt_and_pepper_10_median_3x3.jpeg', salpep_10_med_3)
fp.write("salt and pepper 0.1 3x3 median filter SNR:" + str(SNR(img, salpep_10_med_3)) + '\n')

salpep_10_med_5 = median_filter(salpep_10, 5)
cv2.imwrite('lena_salt_and_pepper_10_median_5x5.jpeg', salpep_10_med_5)
fp.write("salt and pepper 0.1 5x5 median filter SNR:" + str(SNR(img, salpep_10_med_5)) + '\n')

salpep_10_open_close = open_close(kernel, salpep_10)
cv2.imwrite('lena_salt_and_pepper_10_open_close.jpeg', salpep_10_open_close)
fp.write("salt and pepper 0.1 opening then closing SNR:" + str(SNR(img, salpep_10_open_close)) + '\n')

salpep_10_close_open = close_open(kernel, salpep_10)
cv2.imwrite('lena_salt_and_pepper_10_close_open.jpeg', salpep_10_close_open)
fp.write("salt and pepper 0.1 closing then opening SNR:" + str(SNR(img, salpep_10_close_open)) + '\n')

# Generate timestamp of logfile
nowtime = datetime.datetime.now()
fp.write("Log Generated:" + str(nowtime.year) + '/'+ str(nowtime.month) + '/' + str(nowtime.day))
fp.write(' ' + str(nowtime.hour) + ':' + str(nowtime.minute) + ':' + str(nowtime.second) + '\n' + '\n')
fp.close()