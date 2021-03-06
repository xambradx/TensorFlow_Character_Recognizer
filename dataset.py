'''
A module that handles the character dataset.
As images are normally repesented as a 3-dimensional matrix, 
this module would flatten it into a 2-dimensional array/matrix.
Each input would be paired with a separate array of integers (stored separately)
which represents the expected outcome. The input and expected outcome pair 
mirror each others' position, that is that an input at index 'i' inside the 
input list would find its expected outcome pair at index 'i' inside the 
expected outcomes list.

Author: Jose Karol M. Tumulak
Date: 09/05/17 
'''

import os               
import cv2
import numpy as numpy

MAX_PIXEL_THRESHOLD = 255
HALF_PIXEL_THRESHOLD = MAX_PIXEL / 2

# Key: character, Value: expected outcome of the character
expected_outcomes = {
    '0' : [0, 0, 0, 0, 0, 0],
    '1' : [1, 0, 0, 0, 0, 0],
    '2' : [0, 1, 0, 0, 0, 0],
    '3' : [1, 1, 0, 0, 0, 0],
    '4' : [0, 0, 1, 0, 0, 0],
    '5' : [1, 0, 1, 0, 0, 0],
    '6' : [0, 1, 1, 0, 0, 0],
    '7' : [1, 1, 1, 0, 0, 0],
    '8' : [0, 0, 0, 1, 0, 0],
    '9' : [1, 0, 0, 1, 0, 0]
}

# Get the entires dataset in the sub directory 'datasets'
# Returns a tuple in the form of (data_inputs, data_expected)
def get_dataset(dir_path = os.getcwd() + '\datasets', notify=False):
    # container variables to be returned
    inputs = []
    expected = []

    # iterates over all subdirectories, each containing a single type of characater in various fonts
    for root, dirs, files in os.walk(dir_path):

        # iterates over all character subdirectories
        for character in dirs: 

            # notifies caller which character is currently being loaded if notify is flagged True
            if notify:
                print('Loading', character + '\'s...') 

            # creates character subdirectory's full path
            folder_dir = dir_path + '\\' + character 
            # stores the expected output of all inputs with this subdirectory
            expected_outcome = expected_outcomes[character]

            for sub_root, sub_dir, image_files in os.walk(folder_dir):

                # iterates over all fonts of the current character
                for image_file in image_files:

                    # full path of the current image
                    image_dir = sub_root + '\\' + image_file

                    # appends the input and expected outcome into their respective lists
                    inputs.append(get_input(image_dir))
                    expected.append(expected_outcome)
    
    # returns a tuple composed of inputs and expected outcomes
    return (inputs, expected)

# Parses an image for its pixels and returns an array of integers.
# Receives the images full path.
# Returns the images pixel values as an array composed of 1's or 0's.
def get_input(image_dir):
    # container variable to be returned
    inputs = []

    # reads the desired image as greyscale
    # each pixel is a single integer between 0 to 255.
    image = cv2.imread(image_dir, cv2.IMREAD_GRAYSCALE)
    
    # gets the image's width and height
    width, height = image.shape

    # iterates over all of the image's pixels in a left-to-right, top-to-bottom fashion
    for w in range(width):
        for h in range(height):
            # appends a 1 or 0 based on the pixel's value
            inputs.append(resolve_pixel(image[w, h]))

    # returns an array of 1's or 0's
    return inputs

# A hard limiting function for a pixels value
# Returns a 1 or 0
def resolve_pixel(pixel): 
    # if the pixel is darker/less than half of the highest pixel value, returns 1
    # else if it's light/greater, returns 0
    return 1 if pixel <= HALF_PIXEL else 0