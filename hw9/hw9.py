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

border_img_2 = np.zeros((height + 4, width + 4), dtype = np.uint8)
for i in range(height + 2):
    for j in range(width + 2):
        border_img_2[i + 1, j + 1] = border_img[i, j]

for i in range(height + 2):
    border_img_2[i + 1, 0] = border_img[i, 0]
    border_img_2[i + 1, width + 3] = border_img[i, width]

for j in range(width + 2):
    border_img_2[0, j + 1] = border_img[0, j]
    border_img_2[height + 3, j + 1] = border_img[height, j]

border_img_2[0, 0] = border_img[0, 0]
border_img_2[0, width + 3] = border_img[0, width]
border_img_2[height + 3, 0] = border_img[height, 0]
border_img_2[height + 3, width + 3] = border_img[height, width]

def Roberts(border_img, threshold):
    rob = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width):
            r1 = int(border_img[i + 2, j + 2]) - int(border_img[i + 1, j + 1])
            r2 = int(border_img[i + 2, j + 1]) - int(border_img[i + 1, j + 2])
            mask = math.sqrt(math.pow(r1, 2) + math.pow(r2, 2))
            if (mask >= threshold):
                rob[i, j] = 0
            else:
                rob[i, j] = 255
    return rob

def Prewitt(border_img, threshold):
    pew = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width):
            p1 = int(border_img[i + 2, j]) + int(border_img[i + 2, j + 1]) + int(border_img[i + 2, j + 2]) -\
                 int(border_img[i, j]) - int(border_img[i, j + 1]) - int(border_img[i, j + 2])
            p2 = int(border_img[i, j + 2]) + int(border_img[i + 1, j + 2]) + int(border_img[i + 2, j + 2]) -\
                 int(border_img[i, j]) - int(border_img[i + 1, j]) - int(border_img[i + 2, j])
            mask = math.sqrt(math.pow(p1, 2) + math.pow(p2, 2))
            if (mask >= threshold):
                pew[i, j] = 0
            else:
                pew[i, j] = 255
    return pew

def Sobel(border_img, threshold):
    sbl = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width):
            s1 = int(border_img[i + 2, j]) + int(border_img[i + 2, j + 1]) * 2 + int(border_img[i + 2, j + 2]) -\
                 int(border_img[i, j]) - int(border_img[i, j + 1]) * 2 - int(border_img[i, j + 2])
            s2 = int(border_img[i, j + 2]) + int(border_img[i + 1, j + 2]) * 2 + int(border_img[i + 2, j + 2]) -\
                 int(border_img[i, j]) - int(border_img[i + 1, j]) * 2 - int(border_img[i + 2, j])
            mask = math.sqrt(math.pow(s1, 2) + math.pow(s2, 2))
            if (mask >= threshold):
                sbl[i, j] = 0
            else:
                sbl[i, j] = 255
    return sbl

def FreiandChen(border_img, threshold):
    fnc = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width):
            f1 = int(border_img[i + 2, j]) + int(border_img[i + 2, j + 1]) * math.sqrt(2) + int(border_img[i + 2, j + 2]) -\
                 int(border_img[i, j]) - int(border_img[i, j + 1]) * math.sqrt(2) - int(border_img[i, j + 2])
            f2 = int(border_img[i, j + 2]) + int(border_img[i + 1, j + 2]) * math.sqrt(2) + int(border_img[i + 2, j + 2]) -\
                 int(border_img[i, j]) - int(border_img[i + 1, j]) * math.sqrt(2) - int(border_img[i + 2, j])
            mask = math.sqrt(math.pow(f1, 2) + math.pow(f2, 2))
            if (mask >= threshold):
                fnc[i, j] = 0
            else:
                fnc[i, j] = 255
    return fnc

def Kirsch(border_img, threshold):
    kir = np.zeros((height, width), dtype = np.uint8)
    k1 = np.array([[-3, -3, 5],\
                    [-3, 0, 5],\
                   [-3, -3, 5]])
    k2 = np.array([[-3, 5, 5],\
                    [-3, 0, 5],\
                   [-3, -3, -3]])
    k3 = np.array([[5, 5, 5],\
                    [-3, 0, -3],\
                   [-3, -3, -3]])
    k4 = np.array([[5, 5, -3],\
                    [5, 0, -3],\
                   [-3, -3, -3]])
    k5 = np.array([[5, -3, -3],\
                    [5, 0, -3],\
                   [5, -3, -3]])
    k6 = np.array([[-3, -3, -3],\
                    [5, 0, -3],\
                   [5, 5, -3]])
    k7 = np.array([[-3, -3, -3],\
                    [-3, 0, -3],\
                   [5, 5, 5]])
    k8 = np.array([[-3, -3, -3],\
                    [-3, 0, 5],\
                   [-3, 5, 5]])

    for i in range(height):
        for j in range(width):
            val = np.zeros((8), dtype = np.int32)
            for m in range(3):
                for n in range(3):
                    val[0] += k1[m, n] * int(border_img[i + m, j + n])
                    val[1] += k2[m, n] * int(border_img[i + m, j + n])
                    val[2] += k3[m, n] * int(border_img[i + m, j + n])
                    val[3] += k4[m, n] * int(border_img[i + m, j + n])
                    val[4] += k5[m, n] * int(border_img[i + m, j + n])
                    val[5] += k6[m, n] * int(border_img[i + m, j + n])
                    val[6] += k7[m, n] * int(border_img[i + m, j + n])
                    val[7] += k8[m, n] * int(border_img[i + m, j + n])
            max = val[0]
            for k in range(8):
                if (val[k] > max):
                    max = val[k]
            if (max >= threshold):
                kir[i, j] = 0
            else:
                kir[i, j] = 255
    return kir

def Robinson(border_img, threshold):
    rbn = np.zeros((height, width), dtype = np.uint8)
    k1 = np.array([[-1, 0, 1],\
                   [-2, 0, 2],\
                   [-1, 0, 1]])
    k2 = np.array([[0, 1, 2],\
                   [-1, 0, 1],\
                   [-2, -1, 0]])
    k3 = np.array([[1, 2, 1],\
                    [0, 0, 0],\
                   [-1, -2, -1]])
    k4 = np.array([[2, 1, 0],\
                    [1, 0, -1],\
                   [0, -1, -2]])
    k5 = np.array([[1, 0, -1],\
                   [2, 0, -2],\
                   [1, 0, -1]])
    k6 = np.array([[0, -1, -2],\
                    [1, 0, -1],\
                   [2, 1, 0]])
    k7 = np.array([[-1, -2, -1],\
                    [0, 0, 0],\
                   [1, 2, 1]])
    k8 = np.array([[-2, -1, 0],\
                    [-1, 0, 1],\
                   [0, 1, 2]])

    for i in range(height):
        for j in range(width):
            val = np.zeros((8), dtype = np.int32)
            for m in range(3):
                for n in range(3):
                    val[0] += k1[m, n] * int(border_img[i + m, j + n])
                    val[1] += k2[m, n] * int(border_img[i + m, j + n])
                    val[2] += k3[m, n] * int(border_img[i + m, j + n])
                    val[3] += k4[m, n] * int(border_img[i + m, j + n])
                    val[4] += k5[m, n] * int(border_img[i + m, j + n])
                    val[5] += k6[m, n] * int(border_img[i + m, j + n])
                    val[6] += k7[m, n] * int(border_img[i + m, j + n])
                    val[7] += k8[m, n] * int(border_img[i + m, j + n])
            max = val[0]
            for k in range(8):
                if (val[k] > max):
                    max = val[k]
            if (max >= threshold):
                rbn[i, j] = 0
            else:
                rbn[i, j] = 255
    return rbn

def NevatiaBabu(border_img_2, threshold):
    nev = np.zeros((height, width), dtype = np.uint8)
    n1 = np.array([[100, 100, 100, 100, 100],\
                   [100, 100, 100, 100, 100],\
                   [0, 0, 0, 0, 0],\
                   [-100, -100, -100, -100, -100],\
                   [-100, -100, -100, -100, -100]])
    n2 = np.array([[100, 100, 100, 100, 100],\
                   [100, 100, 100, 78, -32],\
                   [100, 92, 0, -92, -100],\
                   [32, -78, -100, -100, -100],\
                   [-100, -100, -100, -100, -100]])
    n3 = np.array([[100, 100, 100, 32, -100],\
                   [100, 100, 92, -78, -100],\
                   [100, 100, 0, -100, -100],\
                   [100, 78, -92, -100, -100],\
                   [100, -32, -100, -100, -100]])
    n4 = np.array([[-100, -100, 0, 100, 100],\
                   [-100, -100, 0, 100, 100],\
                   [-100, -100, 0, 100, 100],\
                   [-100, -100, 0, 100, 100],\
                   [-100, -100, 0, 100, 100]])
    n5 = np.array([[-100, 32, 100, 100, 100],\
                   [-100, -78, 92, 100, 100],\
                   [-100, -100, 0, 100, 100],\
                   [-100, -100, -92, 78, 100],\
                   [-100, -100, -100, -32, 100]])
    n6 = np.array([[100, 100, 100, 100, 100],\
                   [-32, 78, 100, 100, 100],\
                   [-100, -92, 0, 92, 100],\
                   [-100, -100, -100, -78, 32],\
                   [-100, -100, -100, -100, -100]])
    for i in range(height):
        for j in range(width):
            val = np.zeros((6), dtype = np.int32)
            for m in range(5):
                for n in range(5):
                    val[0] += n1[m, n] * int(border_img_2[i + m, j + n])
                    val[1] += n2[m, n] * int(border_img_2[i + m, j + n])
                    val[2] += n3[m, n] * int(border_img_2[i + m, j + n])
                    val[3] += n4[m, n] * int(border_img_2[i + m, j + n])
                    val[4] += n5[m, n] * int(border_img_2[i + m, j + n])
                    val[5] += n6[m, n] * int(border_img_2[i + m, j + n])
            max = val[0]
            for k in range(6):
                if (val[k] > max):
                    max = val[k]
            if (max >= threshold):
                nev[i, j] = 0
            else:
                nev[i, j] = 255
    return nev

img_roberts = Roberts(border_img, 30)
cv2.imwrite('lena_Roberts_30.jpeg', img_roberts)

img_prewitt = Prewitt(border_img, 24)
cv2.imwrite('lena_Prewitt_24.jpeg', img_prewitt)

img_sobel = Sobel(border_img, 38)
cv2.imwrite('lena_Sobel_38.jpeg', img_sobel)

img_freiandchen = FreiandChen(border_img, 30)
cv2.imwrite('lena_Frei_and_Chen_30.jpeg', img_freiandchen)

img_kirsch = Kirsch(border_img, 135)
cv2.imwrite('lena_Kirsch_135.jpeg', img_kirsch)

img_robinson = Robinson(border_img, 43)
cv2.imwrite('lena_Robinson_43.jpeg', img_robinson)

img_nevatia_babu = NevatiaBabu(border_img_2, 12500)
cv2.imwrite('lena_Nevatia_Babu_12500.jpeg', img_nevatia_babu)