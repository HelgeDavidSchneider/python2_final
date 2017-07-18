"""
Helge Schneider, 3925188
Please use Project with Python 3.5

1. Define all functions
2. Use the incredible_filter function with the wanted variables

Please consider that the calculation takes very long for large images, especially the wedge filter needs a lot of time
incredible_filter uses a mirrowed edge padding for the calculations

Questions for next lesson
What ist the best way to store extracted data from different arrays?
how can i extract a row from array without a single element?
how to deal with uneven positions?
"""

import numpy as np
import scipy
from scipy.misc import imread
from math import sqrt
import matplotlib.pyplot as plt
import sympy
from sympy import *


def incredible_filter(img_path, filtertype="square", functiontype="mean", squarelength=None, shape=None, radius=None,
               angles=None):
    if filtertype == "square":
        if isinstance(squarelength, int):
            return img_filter(img_path=img_path, filtertype=filtertype, squarelength=squarelength,
                              shape=shape, radius=radius, angles=angles, functiontype=functiontype)
        else:
            raise TypeError('Squarelength not known\nPlease provide the squarelength as an integer\n'
                            'For example: squarelength = 3')

    elif filtertype == "rectangular":
        if isinstance(shape, tuple) and len(shape) == 2:
            return img_filter(img_path=img_path, filtertype=filtertype, squarelength=squarelength,
                              shape=shape, radius=radius, angles=angles, functiontype=functiontype)
        else:
            raise TypeError('Shape not known\nPlease provide the shape as a tuple\nFor example: shape = (4,3)')

    elif filtertype == "circle":
        if isinstance(radius, int):
            return img_filter(img_path=img_path, filtertype=filtertype, squarelength=squarelength,
                              shape=shape, radius=radius, angles=angles, functiontype=functiontype)
        else:
            raise TypeError('Radius not known\nPlease provide the radius as an integer\nFor example: radius = 4')

    elif filtertype == "wedge":
        if isinstance(angles, tuple) and len(angles) == 3:
            return img_filter(img_path=img_path, filtertype=filtertype, squarelength=squarelength,
                              shape=shape, radius=radius, angles=angles, functiontype=functiontype)
        else:
            raise TypeError('Angles not known\nPlease provide the radius and the start/end angle as a tuple\n'
                            'For example: angles = (3, 0, 90)')

    else:
        raise TypeError(
            'type: %s not known\nPlease provide one of the following types:\n"square","rectangular","circle","wedge"' % (
            filtertype))


def img_filter(img_path, filtertype, functiontype="mean", squarelength=None, shape=None, radius=None, angles=None):
    # save image as numpy array
    img_org = scipy.misc.imread(img_path, flatten=False, mode=None)

    # create  new empty array for the filtered image
    img_fil = np.zeros(img_org.shape, dtype=np.uint8)

    # filter all layers
    for layer in range(3):
        img_fil[:, :, layer] = layerfilter(layer=img_org[:, :, layer], filtertype=filtertype,
                                           squarelength=squarelength, shape=shape, radius=radius, angles=angles,
                                           functiontype=functiontype)

    # konvert the image to uint 8
    img_fil = img_fil.astype(np.uint8)

    # plot the image
    plt.imshow(img_fil)

    # return the filtered image
    return img_fil


def layerfilter(layer, filtertype, functiontype, squarelength, shape, radius, angles):

    # calculate the needed pad_width for each type and difine the functions with arguments for better performance
    if filtertype == "square":
        padwidth = int(squarelength / 2)
        filterfunktion = squarefilter
        argument = squarelength

    if filtertype == "rectangular":
        padwidth = int(max((shape[0], shape[1])) / 2)
        filterfunktion = rectangularfilter
        argument = shape

    if filtertype == "circle":
        padwidth = radius
        filterfunktion = circlefilter
        argument = radius

    if filtertype == "wedge":
        padwidth = angles[0]
        filterfunktion = wedgefilter
        argument = angles

    if functiontype == "max":
        method = max

    if functiontype == "min":
        method = min

    if functiontype == "mean":
        method = np.mean

    if functiontype == "std":
        method = np.std

    if functiontype == "var":
        method = np.var

    # create the new layer for the filtered image
    newlayer = np.zeros(shape=layer.shape, dtype=np.uint8)

    # add a pad to the original layer to be able to iterate over it
    layer = np.pad(layer, padwidth, mode="symmetric")  # pad the original layer

    # iterate over the layer without the padding, window is a square with 2*pad+1 width (central pixel + radius)
    for i in range(newlayer.shape[0]):  # iterate over rows
        for j in range(newlayer.shape[1]):  # iterate over columns
            # extract the window around the pixel
            window = layer[i:(i + padwidth * 2) + 1, j:(j + padwidth * 2) + 1]
            # get all the neighbour values from the window with the wanted function
            window_values = filterfunktion(window, argument)
            # pixelvalue = getattr(np, func)(window_values)
            pixelvalue = method(window_values)
            # print(pixelvalue)
            newlayer[i, j] = pixelvalue

    return newlayer


def squarefilter(image, squarelength):
    all_values = image.flatten().tolist()
    middle = int((len(all_values)) / 2)
    values = all_values[:middle] + all_values[middle + 1:]
    return values


def rectangularfilter(image, shape):
    # the function gets a square as image with the wanted pixel in the middle
    # if a number of shape is not an even number some more rows are included for the calculation
    r_diff = int((image.shape[0] - shape[0]) / 2)
    c_diff = int((image.shape[0] - shape[1]) / 2)
    # just do it if index = 0, otherwise there are problem with the slicing
    if r_diff != 0:
        image = image[r_diff:-r_diff, :]
    if c_diff != 0:
        image = image[:, c_diff:-c_diff]

    # get all values as a flatted list
    all_values = image.flatten().tolist()
    # delete the value in the middle
    middle = int((len(all_values) - 1) / 2)

    # keep all other values
    values = all_values[:middle] + all_values[middle + 1:]

    return values


def circlefilter(image, radius):
    """
    image must be square width edge length 2*radius+1
    returns value of the wanted window
    """

    # prepare list to store the wanted values of every row
    neighbours = list(range(image.shape[0]))

    # get the values from the middle row without the center
    neighbours[0] = np.concatenate((image[radius, :radius], image[radius, radius + 1:])).tolist()

    # index to iterate over the list
    index = 1

    # iterate from the middle row up and down until the top/bottom
    for i in range(1, radius + 1):
        # calculate the index of the first cell which is included in the circle
        included = radius - int(sqrt(radius ** 2 - i ** 2))
        # create a list of all included values in the row above and below
        neighbours[index] = image[radius + i][included: -included].tolist()  # values above
        index += 1
        neighbours[index] = image[radius - i][included: -included].tolist()  # values below
        index += 1
    # flat the list
    values = [v for a in neighbours for v in a]
    return values


def wedgefilter(image, angles):
    # get the index of the wanted value
    middle = int(image.shape[0] / 2)
    # create the zero degree line
    reference = Line(Point(middle, middle), Point(middle + 1, middle))
    # create list for the neighbourhood values
    values = list()

    # iterate through all the values and check if the angle is betwen start and end angle
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # skip central point
            if i == j == middle:
                continue
            # row value ~ y value, column value ~ x value
            pline = Line(Point(middle, middle), Point(j, i))
            # calculate angle in degree
            angle = (reference.angle_between(pline) / (2 * sympy.pi)) * 360
            if i < middle:
                angle = 360 - angle
            distance = sqrt(((image.shape[0] - 1 - i) - middle) ** 2 + (j - middle) ** 2)
            if angles[1] <= angle <= angles[1] and distance <= angles[2]:
                values.append(image[image.shape[0] - 1 - i, j])
    return values


# For example:
img_path = 'C:/Users/helge/Dropbox/Uni/Python 2/material/images/apple.jpg'
mean_img = incredible_filter(img_path, filtertype="square", squarelength =2, functiontype="std")