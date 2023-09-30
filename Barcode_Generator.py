#create a folder called matches in the same directory before starting

from cv2 import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import skimage.transform as ski

def get_images():
    
    
    cropped = np.empty((0,18,18))

    # Iterates through each folder to obtain the image, and crop it
    for i in range(0,10,1):
        for filename in os.listdir('MNIST_DS\\{}'.format(i)):
            img = cv2.imread(os.path.join('MNIST_DS\\{}'.format(i),filename),0)
            if img is not None:
                preImg = np.array(img)
                postImg = preImg[5:23,5:23] # crops image to rows+columns 5-23, to eliminate blank space
                cropped = np.append(cropped,[postImg], axis=0)
    return cropped

# Obtains the original image from an provided index.
def get_image(index):
    filename = os.listdir('MNIST_DS\\{}'.format(int(index/10)))
    img = cv2.imread(os.path.join('MNIST_DS\\{}'.format(int(index/10)),filename[int((str(index))[-1])]),0)
    if img is not None:
        return img

# Creates the barcode for an image
def create_code(image):
    #Radon method
    code = np.array([])
    for i in range(0,180,15): # Specifies the start, stop, step for projection degrees
        projection = ski.radon(image,[i],circle=True,preserve_range=True)
        threshold = np.mean(projection)          
        for i in range(0,projection.size,1):
            if (projection[i]>=threshold):
                projection[i] = 1
            else:
                projection[i] = 0

        code = np.append(code,projection)

    # converts code from array to string
    codeString = ''
    for i in range(0,code.size,1):
        codeString += str(int(code[i]))

    return codeString

# Runs the corresponding functions to generate the codes for the dataset
def create_code_set():
    # create if doesn't exist or open if file does exist
    try:
        f = open("codes.txt", "x")
    except:
        f = open("codes.txt", "w")

    # get array of all images
    images = get_images()
    
    # reshapes the array
    num_images = images.shape[0]    
    # for all images create a code and write it to txt file
    for index in range(0,num_images,1):
        code_string = create_code(np.asarray(images[index]))
        f.write(code_string +'\n')

    f.close()

# Generates the code set for first use.
create_code_set()
print("Setup complete.")
