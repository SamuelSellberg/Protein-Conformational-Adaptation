# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 17:32:23 2019

@author: Samuel P. Sellberg
"""


from scipy import *


def primRec(function,ρ,N,i=0,a=None,returnIndex=False):
    """Iterates primitive recursion of a defined function in a set number 
of times.

Parameters
----------
function : callable function
    The function must imitate the following; function(input,i,a,...),
    even if it only uses the first input.
    The function is used in a recursive loop a set number of times, 
    because of this, the function must return the same type as the expected 
    input.
    An example of such a functuon would be:
        
        fuction(input,i,a):
            return input + a[i]
    
    which would be the same as Σ(a[k]),
    or:
    
        function(input,i,a):
            return input * a(i)
    
    which would be the same as Π(a(k)).
ρ : any
    The initial values that get used as 'input' in 'function' the first 
    iteration. Should be of the expected type of the parameter 'input'
    in 'function'.
N : integer or callable function
    The set number of times the iteration will exceed. The index will grow 
    until it reaches this value.
    If used as a function, the 'N'-function must imitate N(input,i,a,...), 
    even if it only uses the first input.
    The 'N'-function is used as a comparison expression and must return a 
    boolean. Each result from every iteration will be compared in the 
    'N'-function, and when the 'N'-function returns True the iteration will 
    stop.
    An example of such a 'N'-function would be:
    
        N(input,i,a):
            return input >= 3
    
    which would stop the iteration when the result reaches 3.
    By using 'i' and 'a', other comparisons can be made:
    
        N(input,i,a):
            return input >= a[i]
    
    which would stop the iteration when the result surpasses the values of 
    serie a.
i : integer, optional
    The index of which the iteration will start.
    This index will then increase for each iteration and inserted to each 
    function as the parameter 'i'.
a : any, optional
    Will act as the input 'a' to each function of the iteration, therefore 
    it should be of the type expected in 'function'.
    If 'a' is an iterable object, 'a' should contain at least as many items 
    as the value of 'N'.
returnIndex : bool, optional
    When False, it returns the calculated result.
    When True, it returns the index. This is only used when 'N' is used as a 
    comparison expression.

Returns
-------
result : any or integer
    When 'returnIndex = False', the result will be of the same type as the 
    input parameter 'ρ'. This is the resulting value of the intended number 
    of iterations of the function 'function'.
    When 'returnIndex = True', the result will be an integer. This is the 
    resulting index of the number of iterations.

See Also
--------
nestledTensor : Nestled indexation of a tensor of an arbitrary dimension.

Notes
-----
'returnIndex = True' should only be used when 'N' is used as a comparison 
expression. Otherwise, it will just return the 'N' value.

When 'N' is used as a comparison expression, the recursive function may need 
to be interrupted manually as the runtime may not stop, 
given the N-comparison.
By defining the 'N'-function to print the result of every iteration or the 
differentiation within the comparison in the console, 
the never ending runtime can be monitored.
    """
    if not callable(function):
        raise TypeError("'function' must be callable.")
    if not callable(N) and not isinstance(N,int):
        raise TypeError("'N' must be of type integer or a callable function.")
    if not isinstance(i,int):
        raise TypeError("Index 'i' must be of type integer.")
    if not isinstance(returnIndex,bool):
        raise TypeError("'returnIndex' must be of type boolean.")
    if i <= 0:
        raise ValueError("Index 'i' must be positive.")
    result = ρ
    if isinstance(N,int):
        if N <= 0:
            raise ValueError("'N' must be positive.")
        for i in range(i,N):
            result = function(result,i,a)
    if callable(N):
        while(N(result,i,a)):
            result = function(result,i,a)
            i += 1
    if returnIndex == True:
        return i
    return result


def nestledTensor(dimension,size,function,constants=None,varlist=[]):
    """Nestled indexation of a tensor of an arbitrary dimension.

Parameters
----------
dimension : integer
    The number of dimensions the iteration should considerate. 
    Must correspond to the number of elements in 'size'.
size : integer or list of, tuple of, or array of integers
    The size of the tensor, i.e. the boundries of the indexation in each 
    dimension. Must contain as many elements as the number of dimensions.
function : callable function
    The inner function of the nestled loops. This function must imitate the 
    following; function(indexList,constants,...).
    The parameter 'indexList' is a list containing the indices of each 
    dimension, while the parameter 'constants' is simply passed on from the 
    outer 'nestledTensor'-function.
constants : any, optional
    Object passed on as second parameter to the inner function 'function'.
varlist : list or array, optional
    List of initial indices of the next nestled iteration, 
    may leaved empty. Used to add the iterated indexation in each recursive 
    loop of the nestled iteration.

Returns
-------
Nothing : NoneType
    No returns alowed in a nestled recursive loop.
    All changes should be handeled in the inner function 'function' by e.g. 
    performing changes inside a tensor by accessing each element by 
    provision of the indices.

See Also
--------
primRec : Iterates primitive recursion of a defined function in a set number 
of times.

Notes
-----
Optimal usage for applications when the dimensions of a tensor may vary.
When the dimension of a tensor is known and constant, normal nestled loops 
may be of preffered method.
    """
    if not isinstance(dimension,int):
        raise TypeError("'dimension' must be of type integer.")
    if not isinstance(size,(int,tuple,list,ndarray)):
        raise TypeError("'size' must be of type integer, tuple, list, or ndarray.")
    if not callable(function):
        raise TypeError("'function' must be callable.")
    if not isinstance(varlist,(list,ndarray)):
        raise TypeError("'varlist' must be of type list or ndarray.")
    if dimension < 0:
        raise ValueError("'dimensions' must be positive.")
    if dimension > len(size):
        raise ValueError("The 'size'-argument does not match the 'dimension'-argument.")
    if dimension == 0:
        function(varlist,constants)
    else:
        if len(varlist) < len(size):
            varlist.append(0)
        for i in range(size[len(size)-dimension]):
            varlist[len(size)-dimension] = i
            nestledTensor(dimension-1,size,function,constants,varlist)

