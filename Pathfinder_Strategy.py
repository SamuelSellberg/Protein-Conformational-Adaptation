# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 18:25:39 2019

@author: Samuel P. Sellberg
"""

from scipy import floor
from pylab import ndarray, ones
from extendedMath import nestledTensor

import scipy.misc as sm

MAP=sm.imread('noisemap.jpg',True)
MAPfull=sm.imread('newMap.jpg',True)
#sm.imsave('newMap.jpg',MAP)


def pathfinder(tensor,useMark=None):
    if not isinstance(tensor,(list,ndarray)):
        raise TypeError("'pathfinder'-function must have 'list'- or 'ndarray'-object as 'tensor'-argument.")
    if not isinstance(useMark,object):
        raise TypeError("'useMark' must be of type 'object'.")
    
    def neighbourCheck(iterateList,constants):
        val = tensor[tuple(iterateList)]
        for i in range(dimension):
            temp1 = iterateList.copy()
            temp1[i] -= hop
            temp2 = iterateList.copy()
            if iterateList[i] != (shape[i]-1):
                temp2[i] += hop
            else:
                temp2[i] = 0
            if tensor[tuple(temp1)]<val or tensor[tuple(temp2)]<val:
                return
        localMinima.append(iterateList.copy())
    
    dimension = tensor.ndim
    shape = tensor.shape
    localMinima = []
    hop = 1
    nestledTensor(dimension,shape,neighbourCheck)
    if useMark != None:
        for i in localMinima:
            tensor[tuple(i)] = useMark
        return tensor
    return localMinima


def pathfinderChange(tensor):
    if not isinstance(tensor,(list,ndarray)):
        raise TypeError("'pathfinder'-function must have 'list'- or 'ndarray'-object as 'tensor'-argument.")
    
    def neighbourCheck(iterateList,constants):
        val = tensor[tuple(iterateList)]
        for i in range(dimension):
            temp1 = iterateList.copy()
            temp1[i] -= hop
            temp2 = iterateList.copy()
            if iterateList[i] != (shape[i]-1):
                temp2[i] += hop
            else:
                temp2[i] = 0
            if abs(tensor[tuple(temp1)]-val) > maxMin[0]:
                maxMin[0] = abs(tensor[tuple(temp1)]-val)
            if abs(tensor[tuple(temp1)]-val) < maxMin[1]:
                maxMin[1] = abs(tensor[tuple(temp1)]-val)
            if abs(tensor[tuple(temp2)]-val) > maxMin[0]:
                maxMin[0] = abs(tensor[tuple(temp2)]-val)
            if abs(tensor[tuple(temp2)]-val) < maxMin[1]:
                maxMin[1] = abs(tensor[tuple(temp2)]-val)
        return
    
    dimension = tensor.ndim
    shape = tensor.shape
    maxMin = [0,0]
    hop = 1
    nestledTensor(dimension,shape,neighbourCheck)
    return maxMin


def pathfinderPic(tensor,accuracy='full',marked=False):
    if not isinstance(tensor,(list,ndarray)):
        raise TypeError("'pathfinder'-function must have 'list'- or 'ndarray'-object as 'tensor'-argument.")
    if accuracy!='full' and not isinstance(accuracy,int):
        raise TypeError("""'pathfinder'-function 'accuracy'-argument must be "full" or 'int'-object.""")
    if not isinstance(marked,bool):
        raise TypeError("'marked' must be of type 'boolean'")
    if accuracy!='full' and accuracy<0:
        raise ValueError("'pathfinder'-function must have 'accuracy'-argument greater than zero.")
    if accuracy!='full':
        
        def putIn(iterateList):
            for i in range(dimension):
                if iterateList[i]%jumpDim[i]!=0:
                    return
            listOfCompElements.append(tensor[tuple(iterateList)])
        
        def fold(iterateList):
            compTensor[tuple(iterateList)]=listOfCompElements.pop(0)
        
        dimension = tensor.ndim
        shape = tensor.shape
        ac = []
        for i in range(dimension):
            ac.append(accuracy)                 # If dimension == 3 and accuracy == N → ac = (N,N,N)
        compTensor = ones(ac)
        listOfCompElements = []
        jumpDim = []
        for i in range(dimension):
            jumpDim.append(floor((shape[i]-1)/(accuracy-1)))
        nestledTensor(dimension,shape,putIn)
        nestledTensor(dimension,ac,fold)
        tensor = compTensor
    
    def neighbourCheck(iterateList):
        val = tensor[tuple(iterateList)]
        for i in range(dimension):
            temp1 = iterateList.copy()
            temp1[i]-=hop
            temp2 = iterateList.copy()
            if iterateList[i]!=(shape[i]-1):
                temp2[i]+=hop
            else:
                temp2[i] = 0
            if tensor[tuple(temp1)]<val or tensor[tuple(temp2)]<val:
                return
        localMinima.append(iterateList.copy())
    
    dimension = tensor.ndim
    shape = tensor.shape
    localMinima = []
    hop = 1
    nestledTensor(dimension,shape,neighbourCheck)
    if marked==True:
        for i in localMinima:
            tensor[tuple(i)] = 255
        return tensor
    return localMinima


def spottedPic(file,newFile,compress='full'):
    pic=sm.imread(file,True)
    picX=pathfinderPic(pic,compress,True)
    sm.imsave(newFile,picX)

