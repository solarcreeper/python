import sys, random, argparse
import math
import numpy
from PIL import Image

def getAverageL(image):
    im =numpy.array(image)
    w,h = im.shape
    return numpy.average(im.reshape(w*h))

def convertImageToAscii(filename, col, scale):
    image = Image.open(filename).convert('L')
    W = image.size[0]
    H = image.size[1]
    w = W / col
    h = w / scale
    rows = int(H / h)

    aimg = []

    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)
        if j == rows - 1:
            y2 = H

        aimg.append("")
        for i in range(col):
            x1 = int(i * w)
            x2 = int((i + 1) * w)
            if i == col - 1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageL(img))
            gsval = gscale[int((avg*9)/255)]
            aimg[j] = aimg[j] + gsval
    return aimg


gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
col = 100
scale = 0.43

image = convertImageToAscii('test4.jpg', col, scale)

for row in image:
    print(row)
pass