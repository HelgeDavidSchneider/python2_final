"""
3925188 Helge Schneider
Project was created with Python 3.5

Questions for next next lesson:
How to handle zero devision Error with numpy?
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy
from scipy.misc import imread
from math import sqrt, log
import gdal
import numpy as np

# Task 1
"""
Just use the available_equations() function to see the results
"""

def available_equations():
    """
    :return: Plots 20 available indexes for image processing
    """

    # set figure
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)

    # set LaTeX
    mpl.rcParams['text.usetex'] = True

    #title in box
    ax.text(0, 205, '20 available Indexes and their equations', style='italic', fontsize=20,
            bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})

    #20 equations
    ax.text(0, 190, r'1.\t Atmospherically Resistant Vegetation Index 2 (ARVI2):'
                    r' $-0.18+1.17 \biggl(\frac{NIR-RED}{NIR+RED}\biggr)$', fontsize=12)
    ax.text(0, 180, r'2.\t Blue-wide dynamic range vegetation index (BWDRVI):'
                    r' $\frac{0.1(NIR-BLUE}{0.1NIR+BLUE}$', fontsize=12)
    ax.text(0, 170, r'3.\t Chlorophyll Index Green (CIgreen): $\frac{NIR}{GREEN}-1$', fontsize=12)
    ax.text(0, 160, r'4.\t Chlorophyll vegetation index (CVI): $NIR \frac{RED}{GREEN^2}$', fontsize=12)
    ax.text(0, 150, r'5.\t Coloration Index (CI): $\frac{RED-BLUE}{RED}$', fontsize=12)
    ax.text(0, 140, r'6.\t Enhanced Vegetation Index (EVI): $2.5\frac{NIR-RED}{(NIR+6*RED-7.5*BLUE)+1}$', fontsize=12)
    ax.text(0, 130, r'7.\t Enhanced Vegetation Index 2 (EVI2): $2.4\frac{NIR-RED}{NIR+RED+1}$', fontsize=12)
    ax.text(0, 120, r'8.\t Enhanced Vegetation Index 2 -2 (EVI2): $2.5\frac{NIR-RED}{NIR+2.4*RED+1}$', fontsize=12)
    ax.text(0, 110, r'9.\t Green atmospherically resistant vegetation index (GARI): '
                    r'$\frac{NIR-(GREEN-(BLUE-RED))}{NIR-(GREEN+(BLUE-RED))}$', fontsize=12)
    ax.text(0, 100, r'10.\t Green leaf index (GLI): $\frac{2*(GREEN-RED-BLUE}{2*GREEN+RED+BLUE}$', fontsize=12)
    ax.text(0,  90, r'11.\t Green-Blue NDVI(GBNDVI): $\frac{NIR-(GREEN+BLUE}{NIR+(GREEN+BLUE)}$', fontsize=12)
    ax.text(0,  80, r'12.\t Green-Red NDVI (GRNDVI): $\frac{NIR-(GREEN+RED)}{NIR+(GREEN+RED)}$', fontsize=12)
    ax.text(0,  70, r'13.\t Log Ratio (LogR): $\log(\frac{NIR}{RED})$', fontsize=12)
    ax.text(0,  60, r'14.\t Modified Simple Ratio NIR/RED (MSRNir/Red): '
                    r'$\frac{\bigl(\frac{NIR}{RED}\bigr)-1}{\sqrt{\bigl(\frac{NIR}{RED}\bigr)+1}}$', fontsize=12)
    ax.text(0,  50, r'15.\t Modified Soil Adjusted Vegetation Index (MSAVI): '
                    r'$\frac{2*NIR+1-\sqrt{(2*NIR+1)^2-8*(NIR-RED)}}{2}$', fontsize=12)
    ax.text(0,  40, r'16.\t Normalized Difference Green/Red (NGRDI): '
                    r'$\frac{GREEN-RED}{GREEN+RED}$', fontsize=12)
    ax.text(0,  30, r'17.\t Normalized Difference NIR/Blue (BNDVI): '
                    r'$\frac{NIR-BLUE}{NIR+BLUE}$', fontsize=12)
    ax.text(0,  20, r'18.\t Normalized Difference NIR/Green (GNDVI): $\frac{NIR-GREEN}{NIR+GREEN}$', fontsize=12)
    ax.text(0,  10, r'19.\t Normalized Difference NIR/Red (NDVI): $\frac{NIR-RED}{NIR+RED}$', fontsize=12)
    ax.text(0,  0,  r'20.\t Pan NDVI (PNDVI): $\frac{NIR-(GREEN+RED+BLUE)}{NIR+(GREEN+RED+BLUE)}$', fontsize=12)

    #axis
    ax.axis([-10, 150, -10, 215])
    plt.axis('off')
    plt.show()

available_equations()

# Task 2
"""
Please import the image with your own path
in Addition extract the different channels and define all the functions
now you can just call plot_all() to see the results
"""

# Importing the image
img_path = "C:/Users/helge/dropbox/Uni/Python 2/Projects/project4/RGBNIR.tif"
img_temp = gdal.Open(img_path)
img_array = img_temp.ReadAsArray()

# Extracting the different Channels
RED =  img_array[0, :, :]
GREEN = img_array[1, :, :]
BLUE = img_array[2, :, :]
NIR = img_array[3, :, :]

# Defining the index functions
def ARVI2(NIR=NIR, RED=RED):
    index = -0.18 + 1.17 * ((NIR - RED) / (NIR + RED))
    return index


def BWDRVI(NIR=NIR, BLUE=BLUE):
    index = (0.1 * NIR - BLUE) / (0.1 * NIR + BLUE)
    return index


def CIgreen(NIR=NIR, GREEN=GREEN):
    index = NIR / GREEN - 1
    return index


def CVI(NIR=NIR, RED=RED, GREEN=GREEN):
    index = NIR * (RED / GREEN ** 2)
    return index


def CI(RED=RED, BLUE=BLUE):
    index = (RED - BLUE) / RED
    return index


def EVI(NIR=NIR, RED=RED, BLUE=BLUE):
    index = 2.5 * ((NIR - RED) / ((NIR + 6 * RED - 7.5 * BLUE) + 1))
    return index


def EVI2(NIR=NIR, RED=RED):
    index = 2.4 * ((NIR - RED) / (NIR + RED + 1))
    return index


def EVI2_(NIR=NIR, RED=RED):
    index = 2.5 * ((NIR - RED) / (NIR + 2.4 * RED + 1))
    return index


def GARI(NIR=NIR, GREEN=GREEN, BLUE=BLUE, RED=RED):
    index = (NIR - (GREEN - (BLUE - RED))) / (NIR - (GREEN + (BLUE - RED)))
    return index


def GLI(GREEN=GREEN, RED=RED, BLUE=BLUE):
    index = (2 * GREEN - RED - BLUE) / (2 * GREEN + RED + BLUE)
    return index


def GBNDVI(NIR=NIR, GREEN=GREEN, BLUE=BLUE):
    index=(NIR - (GREEN + BLUE)) / (NIR + (GREEN + BLUE))
    return index


def GRNDVI(NIR=NIR, GREEN=GREEN, RED=RED):
    index=(NIR - (GREEN + RED)) / (NIR + (GREEN + RED))
    return index


def MSRNir_Red(NIR=NIR, RED=RED):
    index=(NIR / RED - 1) / ((NIR / RED + 1) ** 0.5)
    return index


def MSAVI(NIR=NIR, RED=RED):
    index=(2 * NIR + 1 - ((2 * NIR + 1) ** 2 - 8 * (NIR - RED)) ** 0.5) / 2
    return index


def NGRDI(GREEN=GREEN, RED=RED):
    index=(GREEN - RED) / (GREEN + RED)
    return index


def BNDVI(NIR=NIR, BLUE=BLUE):
    index = (NIR - BLUE) / (NIR + BLUE)
    return index


def GNDVI(NIR=NIR, GREEN=GREEN):
    index = (NIR - GREEN) / (NIR + GREEN)
    return index


def NDVI(NIR=NIR, RED=RED):
    index = (NIR - RED) / (NIR + RED)
    return index


def PNDVI(NIR=NIR, GREEN=GREEN, RED=RED, BLUE=BLUE):
    index = (NIR - (GREEN + RED + BLUE)) / (NIR + (GREEN + RED + BLUE))
    return index


def SQRT_NIR_RED(NIR=NIR, RED=RED):
    index = (NIR / RED) ** 0.5
    return index


def plot_all():
    plt.imshow(ARVI2())
    plt.figure()
    plt.title("ARVI2")

    plt.imshow(BWDRVI())
    plt.figure()
    plt.title("BWDRVI")

    plt.imshow(CIgreen())
    plt.figure()
    plt.title("CIgreen")

    plt.imshow(CVI())
    plt.figure()
    plt.title("CVI")

    plt.imshow(CI())
    plt.figure()
    plt.title("CI")

    plt.imshow(EVI())
    plt.figure()
    plt.title("EVI")

    plt.imshow(EVI2())
    plt.figure()
    plt.title("EVI2")

    plt.imshow(EVI2_())
    plt.figure()
    plt.title("EVI2")

    plt.imshow(GARI())
    plt.figure()
    plt.title("GARI")

    plt.imshow(GLI())
    plt.figure()
    plt.title("GLI")

    plt.imshow(GBNDVI())
    plt.figure()
    plt.title(GBNDVI)

    plt.imshow(GRNDVI())
    plt.figure()
    plt.title("GRNDVI")

    plt.imshow(MSRNir_Red())
    plt.figure()
    plt.title("MSRNir_Red")

    plt.imshow(MSAVI())
    plt.figure()
    plt.title("MSAVI")

    plt.imshow(NGRDI())
    plt.figure()
    plt.title("NGRDI")

    plt.imshow(BNDVI())
    plt.figure()
    plt.title("BNDVI")

    plt.imshow(GNDVI())
    plt.figure()
    plt.title("GNDVI")

    plt.imshow(NDVI())
    plt.figure()
    plt.title("NDVI")

    plt.imshow(PNDVI())
    plt.figure()
    plt.title("PNDVI")

    plt.imshow(SQRT_NIR_RED())
    plt.figure()
    plt.title("SQRT_NIR_RED")

plot_all()

# Task 3
"""
saver takes a function and a path as arguments
it calculates the image with the given function and saves it in the given path
You can try it with the example below yourself
"""

def saver(func, path):
    """
    Calculates the index of an image with the given function and saves the image in the given path
    :param func: function to apply to the image
    :param path: string containing the path to store the variable at
    """
    index = func()
    scipy.misc.imsave(path_test, index)

path_test = "C:/Users/helge/dropbox/image_test.png"
saver(BWDRVI, path = path_test)
