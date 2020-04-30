import numpy as np
import cv2 as cv2
import matplotlib.pyplot as plt

img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
cv2.imshow('test', img)
img_height = img.shape[0]
img_width = img.shape[1]
count = 0
change = 1
minlabel = -1
freq = np.zeros((256), dtype = np.int32)        # each pixel frequency of appearence
binimg = np.ones((img_height, img_width), dtype = np.uint8) # binary image
labels = np.ones((img_height, img_width), dtype = np.int32) # image labels
for i in range(256):
    freq[i] = 0

# binary image and image label initialization
for i in range(img_height):
    for j in range(img_width):
        val = img[i, j]
        freq[val] += 1
        if val < 128:
            binimg[i, j] = 0
            labels[i, j] = 0
        else:
            binimg[i, j] = 255
            count += 1
            labels[i, j] = count

# write binary image
cv2.imwrite('lena_binary.jpeg', binimg)
cv2.imshow('binary image', binimg)

# histogram calculation and generate PNG file
# img_histo = cv2.calcHist([img], [0], None, [256], [0, 256])
# above is function to generate histogram, but I don't use it here
plt.axis('off')
plt.bar(range(1,257), freq, color = ['black']) # notice that use freq[] to draw histogram
plt.savefig("lena_histogram.png", bbox_inches='tight')
plt.show()

#--------------------------
# connected components
parent = np.arange(count + 100)

while (change):
    change = 0
    # first time Top-down scaning
    for i in range(img_height):
        for j in range(img_width):
            if labels[i, j] != 0:
                minlabel = labels[i, j]
                check = 0
                # check pixel up-left corner
                if i != 0 and j != 0:
                    if (0 < labels[(i - 1), (j - 1)] < minlabel):
                        minlabel = labels[(i - 1), (j - 1)]
                        check = 1
                # check pixel upside
                if i != 0:
                    if (0 < labels[(i - 1), j] < minlabel) and check != 1:
                        minlabel = labels[(i - 1), j]
                        check = 1
                # check pixel up-rught corner
                if i != 0 and j != img_height - 1:
                    if (0 < labels[(i - 1), (j + 1)] < minlabel) and check != 1:
                        minlabel = labels[(i - 1), (j + 1)]
                        check = 1
                # check pixel leftside
                if j != 0:
                    if (0 < labels[i, (j - 1)] < minlabel) and check != 1:
                        minlabel = labels[i ,(j - 1)]
                        check = 1
                # adjust label of current pixel
                if minlabel != labels[i, j]:
                    change = 1
                    tag = labels[i, j]
                    parent[tag] = minlabel
                    labels[i, j] = minlabel
    # second time Top-down scaning
    for i in range(img_height):
        for j in range(img_width):
            if labels[i, j] != 0:
                prt = parent[labels[i, j]]
                # check pixel up-left corner
                if i != 0 and j != 0:
                    if parent[labels[(i - 1), (j - 1)]] != prt:
                        parent[labels[(i - 1), (j - 1)]] = prt
                # check pixel upside
                if i != 0:
                    if parent[labels[(i - 1), j]] != prt:
                        parent[labels[(i - 1), j]] = prt
                # check pixel up-right corner
                if i != 0 and j != img_height - 1:
                    if parent[labels[(i - 1), (j + 1)]] != prt:
                        parent[labels[(i - 1), (j + 1)]] = prt
                # check pixel leftside
                if j != 0:
                    if parent[labels[i, (j - 1)]] != prt:
                        parent[labels[i, (j - 1)]] = prt


# count label frequency
lab_fq = np.zeros((count), dtype = np.int32)
for i in range(img_height):
    for j in range(img_width):
        labels[i, j] = parent[labels[i, j]]
        lab_fq[labels[i, j]] += 1


for k in range(count):
    if k != 0:
        if lab_fq[k] >= 500 and count >= lab_fq[k]:
            top = img_height
            bottom = -1
            left = img_width
            right = -1
            sum_i = 0
            sum_j = 0
            for i in range(img_height):
                for j in range(img_width):
                    if (labels[i, j] == k):
                        sum_i += i
                        sum_j += j
                        if i < top:
                            top = i
                        if i > bottom:
                            bottom = i
                        if j < left:
                            left = j
                        if j > right:
                            right = j
            centroid = np.zeros(2, dtype = np.int32)
            avg_i = round(sum_i / lab_fq[k])
            centroid[0] = avg_i
            avg_j = round(sum_j / lab_fq[k])
            centroid[1] = avg_j
            centroid.astype(np.int32)
            cv2.rectangle(binimg, (left, top), (right, bottom), (127, 0, 0), 3)
            cv2.circle(binimg, (centroid[1], centroid[0]), 6, (127, 0, 0), -1)
            count -= lab_fq[k]
cv2.imwrite('lena_boxes.jpeg', binimg)
cv2.imshow('connected components', binimg)