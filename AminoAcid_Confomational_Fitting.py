# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 03:09:59 2019

@author: Samuel P. Sellberg
"""

import sys
sys.path.insert(0, 'D:\Dokument D\Python Scripts')
from Protein_Conformational_Adaptation import *


def aminoAcidFit(aminoAcid,startCoord,startVec,termCoord,termVec):
    if not isinstance(aminoAcid,str):
        raise TypeError("'aminoAcid must be of type string.")
    
    if aminoAcid.lower() == 'glycine' or aminoAcid.lower() == 'gly' or aminoAcid.lower() == 'g':
        None
    
    elif aminoAcid.lower() == 'alanine' or aminoAcid.lower() == 'ala' or aminoAcid.lower() == 'a':
        None
        
    else:
        raise ValueError("Not a valid amino acid.")
    