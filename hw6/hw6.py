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

result = np.zeros((tiny_img_height, tiny_img_width), dtype=np.uint8)

def h(a1, a2, a3, a4):
    if a1 != a2:
        return 's'
    elif a1 == a3 == a4:
        return 'r'
    else:    
        return 'q'

def f(h1, h2, h3, h4):
    if (h1 == h2 == h3 == h4 == 'r'):
        return 5
    else:
        return ((h1 == 'q') + (h2 == 'q') + (h3 == 'q') + (h4 == 'q'))

######################
# x[7] # x[2] # x[6] #
# x[3] # x[0] # x[1] #
# x[8] # x[4] # x[5] #
######################

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
            result[i, j] = 0
        else:
            result[i,j] = f(h(x[0], x[1], x[6], x[2]), \
                            h(x[0], x[2], x[7], x[3]), \
                            h(x[0], x[3], x[8], x[4]), \
                            h(x[0], x[4], x[5], x[1]))

output_log = open("lena_yokoi.txt", 'w')
for i in range(tiny_img_height):
    for j in range(tiny_img_width):
        if (result[i, j] == 0):
            print(" ", end = " ", file = output_log)
        else:
            print(result[i, j], end = " ", file = output_log)
    print(file = output_log)