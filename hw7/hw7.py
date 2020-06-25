import numpy as np
import cv2

img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
img_height = img.shape[0]
img_width = img.shape[1]

tiny_img_height = int(img_height/8)
tiny_img_width = int(img_width/8)
tiny_binimg = np.zeros((tiny_img_height, tiny_img_width), dtype = np.uint8)

for i in range(tiny_img_height):
    for j in range(tiny_img_width):
        if (img[8*i, 8*j] < 128):
            tiny_binimg[i, j] = 0
        else:
            tiny_binimg[i, j] = 255



def h(a1, a2, a3, a4):
    if a1 != a2:
        return 0
    elif a1 == a3 == a4:
        return 2
    else:    
        return 1

def f(h1, h2, h3, h4):
    if (h1 == h2 == h3 == h4 == 2):
        return 5
    else:
        return ((h1 == 1) + (h2 == 1) + (h3 == 1) + (h4 == 1))

######################
# x[7] # x[2] # x[6] #
# x[3] # x[0] # x[1] #
# x[8] # x[4] # x[5] #
######################


while (True):
    change = False
    yokoi_result = np.zeros((tiny_img_height, tiny_img_width))
    for i in range(tiny_img_height):
        for j in range(tiny_img_width):
            x = np.zeros((9), dtype = np.uint8)
            x[0] = tiny_binimg[i, j]
            if (j+1 >= tiny_img_width):
                x[1] = 0
            else:
                x[1] = tiny_binimg[i, j+1]
            if (i-1 < 0):
                x[2] = 0
            else:
                x[2] = tiny_binimg[i-1, j]
            if (j-1 < 0):
                x[3] = 0
            else:
                x[3] = tiny_binimg[i, j-1]
            if (i+1 >= tiny_img_height):
                x[4] = 0
            else:
                x[4] = tiny_binimg[i+1, j]
            if (i+1 >= tiny_img_height or j+1 >= tiny_img_width):
                x[5] = 0
            else:
                x[5] = tiny_binimg[i+1, j+1]
            if (i-1 < 0 or j+1 >= tiny_img_width):
                x[6] = 0
            else:
                x[6] = tiny_binimg[i-1, j+1]
            if (i-1 < 0 or j-1 < 0):
                x[7] = 0
            else:
                x[7] = tiny_binimg[i-1, j-1]
            if (i+1 >= tiny_img_height or j-1 < 0):
                x[8] = 0
            else:
                x[8] = tiny_binimg[i+1, j-1]
            if (tiny_binimg[i, j] == 0):
                yokoi_result[i, j] = 0
            else:
                h1 = h(x[0], x[1], x[6], x[2])
                h2 = h(x[0], x[2], x[7], x[3])
                h3 = h(x[0], x[3], x[8], x[4])
                h4 = h(x[0], x[4], x[5], x[1])
                yokoi_result[i, j] = f(h1, h2, h3, h4)

    pair_relation = np.zeros((tiny_img_height, tiny_img_width), dtype = np.uint8)
    for i in range(tiny_img_height):
        for j in range(tiny_img_width):
            if (tiny_binimg[i, j] == 0):
                pair_relation[i, j] = 0
            elif (yokoi_result[i, j] != 1):
                pair_relation[i, j] = 2
            else:
                tmp = 0
                if (j+1 < tiny_img_width):
                    if (yokoi_result[i, j+1] == 1):
                        tmp += yokoi_result[i, j+1]
                if (i-1 >= 0):
                    if (yokoi_result[i-1, j] == 1):
                        tmp += yokoi_result[i-1, j]
                if (j-1 >= 0):
                    if (yokoi_result[i, j-1] == 1):
                        tmp += yokoi_result[i, j-1]
                if (i+1 < tiny_img_height):
                    if (yokoi_result[i+1, j] == 1):
                        tmp += yokoi_result[i+1, j]
                if (tmp >= 1):
                    pair_relation[i, j] = 1
                else:
                    pair_relation[i, j] = 2

    for i in range(tiny_img_height):
        for j in range(tiny_img_width):            
            if (pair_relation[i, j] == 1 and tiny_binimg[i, j] == 255):
                q_count = 0
                m = np.zeros((9), dtype = np.uint8)
                m[0] = tiny_binimg[i, j]
                if (j+1 >= tiny_img_width):
                    m[1] = 0
                else:
                    m[1] = tiny_binimg[i, j+1]
                if (i-1 < 0):
                    m[2] = 0
                else:
                    m[2] = tiny_binimg[i-1, j]
                if (j-1 < 0):
                    m[3] = 0
                else:
                    m[3] = tiny_binimg[i, j-1]
                if (i+1 >= tiny_img_height):
                    m[4] = 0
                else:
                    m[4] = tiny_binimg[i+1, j]
                if (i+1 >= tiny_img_height or j+1 >= tiny_img_width):
                    m[5] = 0
                else:
                    m[5] = tiny_binimg[i+1, j+1]
                if (i-1 < 0 or j+1 >= tiny_img_width):
                    m[6] = 0
                else:
                    m[6] = tiny_binimg[i-1, j+1]
                if (i-1 < 0 or j-1 < 0):
                    m[7] = 0
                else:
                    m[7] = tiny_binimg[i-1, j-1]
                if (i+1 >= tiny_img_height or j-1 < 0):
                    m[8] = 0
                else:
                    m[8] = tiny_binimg[i+1, j-1]
                h1 = h(m[0], m[1], m[6], m[2])
                h2 = h(m[0], m[2], m[7], m[3])
                h3 = h(m[0], m[3], m[8], m[4])
                h4 = h(m[0], m[4], m[5], m[1])
                q_count = f(h1, h2, h3, h4)
                if (q_count == 1):
                    tiny_binimg[i, j] = 0
                    change = True
    if (change == False):
        break

cv2.imwrite('lena_thin.jpeg', tiny_binimg)