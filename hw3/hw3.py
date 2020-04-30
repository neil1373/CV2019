import numpy as np
import cv2
import matplotlib.pyplot as plt

# Original image
img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
cv2.imwrite('lena_original.jpeg', img)
cv2.imshow('Original Image', img)
img_height = img.shape[0]
img_width = img.shape[1]

# Histogram Calculation of original img //cv2.calcHist([img], [0], None, [256], [0, 256])
img_histo = np.zeros((256), dtype = np.int32)
for i in range(img_height):
    for j in range(img_width):
        img_histo[img[i, j]] += 1
plt.axis('off')
plt.bar(range(1,257), img_histo, color = ['black'])
plt.savefig("lena_ori_histo.png", bbox_inches='tight')
plt.show()

# Intensity divided by 3
newimg1 = img
for i in range(img_height):
    for j in range(img_width):
        newimg1[i, j] //= 3
cv2.imwrite('lena_inten_div3.jpeg', newimg1)
cv2.imshow('Intensity Divided by 3', newimg1)

# Histogram Calculation of newimg1_histo  //cv2.calcHist([newimg1], [0], None, [256], [0, 256])
newimg1_histo = np.zeros((256), dtype = np.int32)
for i in range(img_height):
    for j in range(img_width):
        newimg1_histo[newimg1[i, j]] += 1
plt.axis('off')
plt.bar(range(1,257), newimg1_histo, color = ['black'])
plt.savefig("lena_inten_div3_histo.png", bbox_inches='tight')
plt.show()

# Histogram equalization from Previous Resulting Image
newimg2 = newimg1
sum = 0
hash = np.zeros((256), dtype = np.uint8)
img_area = img_height * img_width
for k in range (256):
    tmp = newimg1_histo[k] / img_area
    tmp *= 255
    sum += tmp
    hash[k] = np.round(sum)

for i in range(img_height):
    for j in range(img_width):
        newimg2[i, j] = hash[newimg2[i ,j]]
cv2.imwrite('lena_histo_equliz.jpeg', newimg2)
cv2.imshow('Histogram Equlalization', newimg2)

#Histogram calculation from newimg2_histo //cv2.calcHist([newimg2], [0], None, [256], [0, 256])
newimg2_histo = np.zeros((256), dtype = np.int32)
for i in range(img_height):
    for j in range(img_width):
        newimg2_histo[newimg2[i, j]] += 1
plt.axis('off')
plt.bar(range(1,257), newimg2_histo, color = ['black'])
plt.savefig("lena_histo_equliz_histo.png", bbox_inches='tight')
plt.show()