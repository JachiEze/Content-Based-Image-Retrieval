## Libraries  use to get the projection from the images
import os
import pathlib
import re

import matplotlib.pyplot as plt
import numpy
import numpy as np
from PIL import Image

cwd = os.getcwd()  # [ Access to the Main Project folder]
print(cwd)
MNIST_path = os.path.join(cwd, 'MNIST_DS')  # [Access to the MNIST_DS folder ih the main project folder]

print(MNIST_path)

images = os.listdir(MNIST_path)  # [Access to all the images' folder]
print(images)


# Hamming distance to calculate the distance between the user barcode and other barcodes in the file
# def hamming_distance(str1, str2):  # [takes user barcode and other barcodes]
#     h = 0
#     if len(str1) == len(str2):  # [checks if both barcode are equal or not]
#         for c1, c2 in zip(str1, str2):
#             # [calculate hwo many number in both barcode matches]
#             if c1 != c2:
#                 h = h + 1  # [increments each time when the numbers in the barcode doesn't match]
#             return h  # [returns the number of 1's]
#     else:
#         return 0  # [if number matches it return 0]
#

for c in images:  # [iterate over the image folders]
    B1 = []
    images_path = os.path.join(MNIST_path, c)  # [stores the path of the all the images' folder]
    print(images_path)
    for image_path in pathlib.Path(images_path).iterdir():  # [ iterate over the images in the folder]
        path = image_path
        print(path)

        arr = np.array(Image.open(path))  # [stores the images as an array]

        A1 = numpy.sum(arr, axis=1)  # [calculate and store 0 degree projection in A1 array, it calcualte it by
        # adding the elements in the row]
        A1average = sum(A1) / len(A1)  # [Takes the average of the numbers in the A1 array]

        # 90 Degree Projection
        A2 = numpy.sum(arr,
                       axis=0)  # [ Calculates and store 90 degree projection, it calculates it by adding the elemts in each column]

        A2average = sum(A2) / len(A2)  # [Takes the average of the numbers in the A2 array]

        # 45 Degree Projection
        A3 = [np.trace(arr, offset=i) for i in range(-np.shape(arr)[0] + 2, np.shape(arr)[1] - 1)]

        A3average = numpy.average(A3)  # [Takes the average of the numbers in the A3 array]

        A4 = [np.trace(np.fliplr(arr), offset=i) for i in range(-np.shape(arr)[0] + 2, np.shape(arr)[1] - 1)]
        A4average = numpy.average(A4)  # [Takes the average of the numbers in the A4 array]

        # Arrays to store the barcode of each projection

        B1 = []
        B2 = []
        B3 = []
        B4 = []
        h = []
        f = open("barcodes", "a")  # [opens a text file to print all the barcodes]
        # Converting to barcode(0 angle project array)
        for k in range(len(A1)):  # iterates over the number in the A1 array]
            if A1[
                k] <= A1average:  # [checks if the number in that array is less than or equal to average of that array]
                B1.append(0)  # [if it is equal or less than, it adds 0 to the B1 array]
            else:
                B1.append(1)  # [if not then it adds 1 to the array]
        print("B:", B1)

        # in similar way binary code of each projection is formed for one image

        for r in range(len(A2)):
            if A2[r] <= A2average:
                B2.append(0)
            else:
                B2.append(1)
        print("B2:", B2)

        for l in range(len(A3)):
            if A3[l] <= A3average:
                B3.append(0)
            else:
                B3.append(1)
        print("B3:", B3)

        for y in range(len(A4)):
            if A4[y] <= A4average:
                B4.append(0)
            else:
                B4.append(1)
        print("B4:", B4)

        BB = B1 + B2 + B3 + B4  # [ Add all the four binary codes to each other to make one binary code]
        BB1=re.sub(r'[^\w\s]','',str(BB))
        BB2=BB1.replace(" ","")

        print(BB)
        f.write(str(BB2) + '\n')  # [ Print that binary code to the file for each image with image path]
        f.close()  # [ close the file]
