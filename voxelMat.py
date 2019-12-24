# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 21:24:54 2019

@author: Samuel P. Sellberg
"""

from scipy import *
from pylab import *

from extendedMath import *

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def voxelMat(volMatrix,rotation=(30,-60),sliced=0,sliceOrient=2,minColour=(0,200,180,128),maxColour=(255,200,180,128),marker=None,markerColour=(210,90,0,255),compact=True):
    if not isinstance(volMatrix,ndarray):
        raise TypeError("'volMatrix' must be of type 'ndarray'.")
    if not isinstance(rotation,(tuple,list)):
        raise TypeError("'rotation' must be of type 'tuple' or 'list'.")
    if not isinstance(sliced,(int,float)):
        raise TypeError("'sliced' must be of type 'int' or 'float'.")
    if not isinstance(sliceOrient,int):
        raise TypeError("'sliceOrient' must be of type 'int'.")
    if not isinstance(minColour,(tuple,list)):
        raise TypeError("'minColour' must be of type 'tuple' or 'list'.")
    if not isinstance(maxColour,(tuple,list)):
        raise TypeError("'maxColour' must be of type 'tuple' or 'list'.")
    if marker != None and not isinstance(marker,list):
        raise TypeError("'marker' must be of type 'list'.")
    if not isinstance(markerColour,(tuple,list)):
        raise TypeError("'markerColour' must be of type 'tuple' or 'list'.")
    if not isinstance(compact,bool):
        raise TypeError("'compact' must be of type 'bool'.")
    if volMatrix.ndim != 3:
        raise ValueError("'volMatrix must be a volumetric matrix/tensor.")
    if len(rotation) != 2:
        raise ValueError("'rotation' must contain two elements.")
    if sliced < 0 or sliced > 1:
        raise ValueError("'sliced' must be a value between 0 and 1.")
    if sliceOrient < -3 or sliceOrient > 3 or sliceOrient == 0:
        raise ValueError("'sliceOrient' must be 1, 2, 3, -1, -2, or -3.")
    if marker != None:
        if len(marker) > 0:
            if len(marker[0]) != 3:
                raise ValueError("marker(s) does not contain 3 coordinates.")
        else:
            raise ValueError("'marker' list is empty.")
    if len(minColour) < 3 or len(minColour) > 4:
        raise ValueError("'minColour' must contain 3 or 4 elements.")
    if len(maxColour) < 3 or len(maxColour) > 4:
        raise ValueError("'maxColour' must contain 3 or 4 elements.")
    if len(markerColour) < 3 or len(markerColour) > 4:
        raise ValueError("'markerColour' must contain 3 or 4 elements.")
    if len(minColour) == 3:
        if isinstance(minColour,tuple):
            minColour = minColour + tuple([255])
        else:
            minColour.append(255)
    if len(maxColour) == 3:
        if isinstance(maxColour,tuple):
            maxColour = maxColour + tuple([255])
        else:
            maxColour.append(255)
    if len(markerColour) == 3:
        if isinstance(markerColour,tuple):
            markerColour = markerColour + tuple([255])
        else:
            markerColour.append(255)
    if minColour[0] < 0 or minColour[0] > 255 or minColour[1] < 0 or minColour[1] > 255 or minColour[2] < 0 or minColour[2] > 255 or minColour[3] < 0 or minColour[3] > 255:
        raise ValueError("The elements of 'minColour' must be a value between 0 and 255.")
    if maxColour[0] < 0 or maxColour[0] > 255 or maxColour[1] < 0 or maxColour[1] > 255 or maxColour[2] < 0 or maxColour[2] > 255 or maxColour[3] < 0 or maxColour[3] > 255:
        raise ValueError("The elements of 'maxColour' must be a value between 0 and 255.")
    if markerColour[0] < 0 or markerColour[0] > 255 or markerColour[1] < 0 or markerColour[1] > 255 or markerColour[2] < 0 or markerColour[2] > 255 or markerColour[3] < 0 or markerColour[3] > 255:
        raise ValueError("The elements of 'markerColour' must be a value between 0 and 255.")
    def slicer(iL,con):
        if iL[sliceOrient] < shape[sliceOrient]*sliced:
            activeVoxels[tuple(iL)] = not boolean
    def filler(iL,con):
        part = (volMatrix[tuple(iL)]-minVal)/(maxVal-minVal)
        hexNum = '#%02x%02x%02x%02x' % (int(minColour[0]+round(colDiff[0]*part)),int(minColour[1]+round(colDiff[1]*part)),int(minColour[2]+round(colDiff[2]*part)),int(minColour[3]+round(colDiff[3]*part)))
        colour[tuple(iL)] = hexNum
    boolean = True
    if sliceOrient < 0:
        boolean = False
        sliceOrient = abs(sliceOrient)
    sliceOrient -= 1
    shape = volMatrix.shape
    activeVoxels = np.empty(shape,dtype=object)
    colour = activeVoxels.copy()
    activeVoxels.fill(boolean)
    maxVal = volMatrix.max()
    minVal = volMatrix.min()
    colDiff = (maxColour[0]-minColour[0],maxColour[1]-minColour[1],maxColour[2]-minColour[2],maxColour[3]-minColour[3])
    nestledTensor(3,shape,slicer)
    nestledTensor(3,shape,filler)
    markerColour = '#%02x%02x%02x%02x' % tuple(markerColour)
    if marker != None:
        for iL in marker:
            colour[tuple(iL)] = markerColour
    if compact == False:
        exShape = (shape[0]*2-1,shape[1]*2-1,shape[2]*2-1)
        exAcVox = np.empty(exShape,dtype=object)
        exCol = exAcVox.copy()
        exAcVox.fill(False)
        exAcVox[::2,::2,::2] = activeVoxels
        exCol[::2,::2,::2] = colour
        activeVoxels = exAcVox
        colour = exCol
    fig = plt.figure(figsize=(10,8.5))
    ax = fig.gca(projection='3d')#,proj_type = 'ortho'
    ax.voxels(activeVoxels,facecolors=colour)
    ax.view_init(*rotation)
    plt.show()
