"""
focal statistics functions from earlier project
"""

import numpy as np
import scipy
# from scipy.misc import imread
from math import sqrt
import matplotlib.pyplot as plt
import sympy
from sympy import *
from scipy.ndimage import imread


def filter_main(img_path, filtertype="square", functiontype="mean",
                squarelength=None, shape=None, radius=None,
                angles=None):
    """
    Starting function that takes given path to img and checks parameter types
    according to chosen filtertype. Function will end with error message if
    provided paramters are not matching expectiations
    """

    if filtertype == "square":
        if isinstance(squarelength, int):
            return img_filter(img_path=img_path, filtertype=filtertype,
                              squarelength=squarelength,
                              shape=shape, radius=radius, angles=angles,
                              functiontype=functiontype)
        else:
            raise TypeError('Squarelength incorrect\nPlease provide '
                            'the squarelength as an integer\n' +
                            'For example: squarelength = 3')

    elif filtertype == "rectangular":
        if isinstance(shape, tuple) and len(shape) == 2:
            return img_filter(img_path=img_path, filtertype=filtertype,
                              squarelength=squarelength,
                              shape=shape, radius=radius, angles=angles,
                              functiontype=functiontype)
        else:
            raise TypeError(
                'Shape incorrect\nPlease provide the shape as a tuple\nFor '
                'example: shape = (4,3)')

    elif filtertype == "circle":
        if isinstance(radius, int):
            return img_filter(img_path=img_path, filtertype=filtertype,
                              squarelength=squarelength,
                              shape=shape, radius=radius, angles=angles,
                              functiontype=functiontype)
        else:
            raise TypeError(
                'Radius incorrect\nPlease provide the radius as an integer\n'
                'For example: radius = 4')

    elif filtertype == "wedge":
        if isinstance(angles, tuple) and len(angles) == 3:
            return img_filter(img_path=img_path, filtertype=filtertype,
                              squarelength=squarelength,
                              shape=shape, radius=radius, angles=angles,
                              functiontype=functiontype)
        else:
            raise TypeError(
                'Angles incorrect\nPlease provide the radius and the start/'
                'end angle as a tuple\n'
                'For example: angles = (3, 0, 90)')

    else:
        raise TypeError(
            'type: %s not known\nPlease provide one of the following types:'
            '\n"square","rectangular","circle","wedge"' % filtertype)


def img_filter(img_path, filtertype, functiontype="mean", squarelength=None,
               shape=None, radius=None, angles=None):
    """
    filter function that calls layerfilter for each color channel according to
    input paramters set and checked in filter_main
    returns new filtered image
    """

    # convert image to numpy array
    img_org = scipy.ndimage.imread(img_path, flatten=False, mode=None)

    # create new empty array for the filtered image
    img_fil = np.zeros(img_org.shape, dtype=np.uint8)

    # filter through the three color channels with given parameters
    for layer in range(3):
        img_fil[:, :, layer] = layerfilter(layer=img_org[:, :, layer],
                                           filtertype=filtertype,
                                           squarelength=squarelength,
                                           shape=shape, radius=radius,
                                           angles=angles,
                                           functiontype=functiontype)

    # convert the image to uint 8
    img_fil = img_fil.astype(np.uint8)

    # plot the image
    plt.figure(figsize=(20, 10))
    plt.subplot(121)
    plt.imshow(img_org)
    plt.title('Original')
    plt.subplot(122)
    plt.imshow(img_fil)
    plt.title('Image with %s filter' % functiontype)
    plt.show()

    # return the filtered image
    return img_fil


def layerfilter(layer, filtertype, functiontype, squarelength, shape, radius,
                angles):
    """
    called by img_filter to return one filtered color channel at a time.
    Calls filter function accordingly to
    chosen filter type
    """

    # get padwith (frame around the picture), filtertype as string to be
    # called later and paramters of chosen filtertype
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

    # associate function types to actual numpy functions
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
    layer = np.pad(layer, padwidth, mode="symmetric")

    # got through the layer without the padding
    # the window is a square with 2*pad+1 width (central pixel + radius)
    for i in range(newlayer.shape[0]):  # iterate over rows
        for j in range(newlayer.shape[1]):  # iterate over columns
            # extract the window around the pixel
            window = layer[i:(i + padwidth * 2) + 1, j:(j + padwidth * 2) + 1]
            # get all the neighbour values from the window
            window_values = filterfunktion(window, argument)
            # call filter function type to calculate pixel value
            # from neighbour values
            pixelvalue = method(window_values)
            # set new filtered pixel
            newlayer[i, j] = pixelvalue

    return newlayer


def squarefilter(image, squarelength):
    """
    calculates the neighbour values for square filter function
    """

    all_values = image.flatten().tolist()
    middle = int((len(all_values)) / 2)
    values = all_values[:middle] + all_values[middle + 1:]
    return values


def rectangularfilter(image, shape):
    """
    calculates the neighbour values for rectangular filter function
    """

    # the function gets a square as image with the wanted pixel in the middle
    # if a number of shape is not an even number some more rows are included
    # for the calculation
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
    calculates the neighbour values for circle filter function
    image must be square width edge length 2*radius+1
    returns value of the wanted window
    """

    # prepare list to store the wanted values of every row
    neighbours = list(range(image.shape[0]))

    # get the values from the middle row without the center
    neighbours[0] = np.concatenate(
        (image[radius, :radius], image[radius, radius + 1:])).tolist()

    # index to iterate over the list
    index = 1

    # iterate from the middle row up and down until the top/bottom
    for i in range(1, radius + 1):
        # calculate the index of the first cell which is included in the circle
        included = radius - int(sqrt(radius ** 2 - i ** 2))
        # create a list of all included values in the row above and below
        neighbours[index] = image[radius + i][
                            included: -included].tolist()  # values above
        index += 1
        neighbours[index] = image[radius - i][
                            included: -included].tolist()  # values below
        index += 1
    # flat the list
    values = [v for a in neighbours for v in a]
    return values


def wedgefilter(image, angles):
    """
    calculates the neighbour values for wedge filter function
    """

    # get the index of the wanted value
    middle = int(image.shape[0] / 2)
    # create the zero degree line
    reference = Line(Point(middle, middle), Point(middle + 1, middle))
    # create list for the neighbourhood values
    values = list()

    # iterate through all the values and check if the angle is betwen start
    # and end angle
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
            distance = sqrt(
                ((image.shape[0] - 1 - i) - middle) ** 2 + (j - middle) ** 2)
            if angles[1] <= angle <= angles[1] and distance <= angles[2]:
                values.append(image[image.shape[0] - 1 - i, j])
    return values
