# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 01:48:02 2019

@author: Samuel P. Sellberg
"""

from scipy import *
from pylab import *
from extendedMath import *


def jigger(function,listOfIndices,constants,step,accuracy,ext=0.001):
    jiggerdIndices = []
    for indices in listOfIndices:
        result = jig(function,indices,constants,step,accuracy,ext)
#        print('-----Result: '+str(result))
        if not result == False:
            jiggerdIndices.append(result)
    return jiggerdIndices


# Vidareförs av jigger: δ-funktion, [φ1,φ2,φ3,...], [c,d,α,λ,...], step (Förändring av φk), 
# accuracy (I närhet av δ), ext (Tröskelvärde då förändring anses insignifikant)
def jig(function,indices,constants,step,accuracy,ext):    #   Error-handeling
    if not callable(function):
        raise TypeError("")
    if not isinstance(indices,(int,list,tuple)):
        raise TypeError("")
    
    if isinstance(indices,(list,tuple)):
        if len(indices) == 0:
            raise ValueError("'indices' list is empty.")
    
        
    δ = function(indices,constants)
    while(True):
        change = [False]*len(indices)
        insig = [False]*len(indices)
        for i in range(len(indices)):
            pφ = indices.copy()
            pφ[i] += step
            pδ = function(pφ,constants)
            mφ = indices.copy()
            mφ[i] -= step
            mδ = function(mφ,constants)
#            print('∆δ: '+str(abs(pδ-δ)/δ)+', '+str(abs(mδ-δ)/δ))
            if abs(pδ-δ)/δ < ext and abs(mδ-δ)/δ < ext:    # TODO Kan behöva revideras
                insig[i] = True
            if pδ < δ and mδ < δ:
                if pδ <= mδ:
                    indices = pφ
                    δ = pδ
                else:
                    indices = mφ
                    δ = mδ
            elif pδ < δ:
                indices = pφ
                δ = pδ
            elif mδ < δ:
                indices = mφ
                δ = mδ
            else:
                change[i] = True
        if δ <= accuracy:
            return indices
#        print('δ:  '+str(δ))
#        print('Change: '+str(change))
#        print('Insig:  '+str(insig))
        if all(change):
            if all(insig):
                return False
            else:
#                print('--Half--')
                step = step/2

