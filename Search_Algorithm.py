from cv2 import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from Barcode_Generator import *

# Finds the closest match for a single image
def find_one(figures, toFind, foundMatches, saveImg):
    images = figures
    query = toFind
    founds = foundMatches
    saveChoice = saveImg

    print('\narray index: ',query)

    #Make the image to be a 2d array of values
    image = np.asarray(images[query])

    label = int(query/10)
    print('label:',label)

    # convert image to code
    code_string = create_code(image)

    # open data set of barcodes and make an array of all of them
    f = open("codes.txt", "r")
    lines = f.readlines()
    f.close()

    # stores the best match found yet
    distance_store = 1000
    index_store = None
    

    # for each of the lines compare aginst the code
    for k in range(0,len(lines),1):
        line = lines[k]
        line = line[:-1] # ignore the '\n' 
        
        distance = 0
        if len(code_string)!=len(line):
            print("String are not equal")
        else:
            for x,(r,j) in enumerate(zip(line,code_string)):
                if r!=j:
                    distance += 1

        # ignore perfect matches
        if(distance < distance_store and distance != 0):
            distance_store = distance
            index_store = int(k) #type error idk why tho it should be fine without the int() but idk

        
    print('distance:', distance_store)
    print("image string:",code_string)
    print("match string:",lines[index_store][:-1])
    print("number of match found:",int(index_store/10))
    print('True match:',int(index_store/10)==label)
    if(int(index_store/10)==label):
        founds +=1

        # Saves the image if user wants to, for correct match
        if(saveChoice == 1):
            f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
            ax1.imshow(get_image(query))
            ax1.set_title('image')
            ax2.imshow(get_image(index_store))
            ax2.set_title('closest match')
            f.savefig('matches\\{}.png'.format(query), dpi=f.dpi)   
    else:
        # Saves the image if user wants to, for incorrect match
        if(saveChoice == 1):
            f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
            ax1.imshow(get_image(query))
            ax1.set_title('image')
            ax2.imshow(get_image(index_store))
            ax2.set_title('wrong match')
            f.savefig('matches\\{}.png'.format(query), dpi=f.dpi)
    return founds

# Finds the closest match for all of the images (calculates hit ratio)
def find_all(images, foundMatches, saveImg):
    figure = images
    founds = foundMatches
    saveChoice = saveImg

    for i in range(0,figure.shape[0]):
        # for each one of the sample jpgs 
        index = i #random.randrange(0,num_images-1)
        founds = find_one(images, index, founds, saveChoice)
    
    # number of barcodecodes matched correctly
    print("Correct matches:",founds)


# np array of all dataset images as a 18 by 18 matrix
images = get_images()

valid_choice = False

# User UI for choice selection
# Determines what the user wants to do (find a single query image)
while(valid_choice != True):
    print("\nContent Based Image Retrieval for Handwritten Images.")
    print("1. Find matches for all images in the data set \n2. Find matches for a specific query image in the dataset")
    queryChoice = input("Please make your selection (1, or 2): ")

    if(queryChoice == "1"):
        valid_choice = True

    elif(queryChoice == "2"):
        valid_choice = True

    else:
        print("\nError: Invalid Entry. Please enter 1, or 2 to specify your choice. Please try again")

valid_choice = False

# determines if user wants to save matches
while(valid_choice != True):
    print("\nWould you like to save the image(s) of the match(es) found?")
    print("1. Yes \n2. No")
    saveChoice = input("Please make your selection (1, or 2): ")

    # sets user's save setting to correspond with selection
    if(saveChoice == "1"):
        saveChoice = int(saveChoice)
        valid_choice = True

    elif(saveChoice == "2"):
        saveChoice = int(saveChoice)
        valid_choice = True

    else:
        print("\nError: Invalid Entry. Please enter 1, or 2 to specify your choice. Please try again.")
valid_choice = False
foundMatches = 0

# Iterates through dataset and finds the best match for each
if (queryChoice == "1"):
    for i in range(0,images.shape[0]):
        toFind = i
        foundMatches = find_one(images, toFind, foundMatches, saveChoice)
    # number of barcodecodes matched correctly
    print("\nCorrect matches:",foundMatches)

# Takes input for the index of the image to search for and compares it against the entire data set   
else:
    valid_choice = False
    while(valid_choice != True):
        toFind = input("\nEnter the index of the query image you would like to use, 1-100 corresponding with the dataset: ")
        try:
            toFind = int(toFind)
            if(toFind<=100 and toFind>=1):
                toFind -= 1
                valid_choice = True
        except:
            print("\nError: Invalid Entry. Please enter an integer 1-100 specify your choice from the dataset. Please try again.")
    find_one(images, toFind, foundMatches, saveChoice)
