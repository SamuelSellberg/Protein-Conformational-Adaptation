# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 21:52:28 2019

@author: Samuel P. Sellberg
"""

import sys
import logging
from scipy import sin, cos, tan, arcsin, arccos, arctan2, sqrt, pi
from pylab import ndarray, zeros
from matplotlib import pyplot
sys.path.insert(0, 'D:\Dokument D\Python Scripts')
from extendedMath import primRec, nestledTensor
from voxelMat import voxelMat
from Pathfinder_Strategy import pathfinder
from Jiggering_Strategy import jigger


def diamond(cartesian):
    if not isinstance(cartesian,(list,tuple,ndarray)):
        raise TypeError("'cartesian' must be of type list, tuple or ndarray.")
    if len(cartesian) != 3:
        raise ValueError("Input vector must consist of three coordinates.")
    β = arccos(cartesian[2])
    γ = arctan2(cartesian[1],cartesian[0])    # Same as 2*arctan(c[1]/(sqrt(c[0]**2+c[1]**2)+c[0]))
    return [β,γ]


def cone(α,φ,λ):
    if not isinstance(α,(int,float)):
        raise TypeError("'α' must be of type integer or float.")
    if not isinstance(φ,(int,float)):
        raise TypeError("'φ' must be of type integer or float.")
    if not isinstance(λ,(list,tuple)):
        raise TypeError("'λ' must be of type list or tuple.")
    if len(λ) != 2:
        raise ValueError("'λ' must be a vector of two elements.")
    ψ = λ[0]
    ω = λ[1]
    
    while(α < 0):
        α += 2*pi
    while(α >= 2*pi):
        α -= 2*pi
    while(φ < -pi):
        φ += pi
    while(φ >= pi):
        φ -= pi
    while(ψ < 0):
        ψ += pi
    while(ψ >= pi):
        ψ -= pi
    while(ω < -pi):
        ω += pi
    while(ω >= pi):
        ω -= pi
    x = cos(α/2)*sin(ψ)*cos(ω) + sin(α/2)*cos(φ)*cos(ψ)*cos(ω) - sin(α/2)*sin(φ)*sin(ω)
    y = cos(α/2)*sin(ψ)*sin(ω) + sin(α/2)*cos(φ)*cos(ψ)*sin(ω) + sin(α/2)*sin(φ)*cos(ω)
    z = cos(α/2)*cos(ψ) - sin(α/2)*cos(φ)*sin(ψ)
    return [x,y,z]


def conformationBondVector(N,α,φ,λ):    # Den f******ing fungerar!!!!!
    def innerCone(var,i,a):
        return cone(a[0][i],a[1][i],diamond(var))
    A = [α,φ]
    ρ = cone(α[0],φ[0],λ)
    return primRec(innerCone,ρ,N,1,A)


def conformationAtomCoordinates(N,d,α,φ,λ,return_b=False):
    atomPos = [0,0,0]
    for i in range(N):
        b = conformationBondVector(i+1,α,φ,λ)
        atomPos[0] += d[i]*b[0]
        atomPos[1] += d[i]*b[1]
        atomPos[2] += d[i]*b[2]
    if return_b==True:
        return (atomPos,b)
    else:
        return atomPos


def conformationVolumePlot(c,d,α,λ,startCoord,terminalα,terminalλ,terminalCoord,dataPoints=100,rotation=(30,-60),colour='#650c00',onlySurface=False,sliced=False):
    def innerCoord(indexList,const):
        var = indexList.copy()
        for i in range(len(indexList)):
            var[i] = (var[i]*(2*pi)/accuracy)-pi
        atomPos = conformationAtomCoordinates(const[0],const[1],const[2],var,const[3])
        xs.append(atomPos[0])
        ys.append(atomPos[1])
        zs.append(atomPos[2])
    constants = [c,d,α,λ,startCoord,terminalα,terminalλ,terminalCoord]
    xs = []
    ys = []
    zs = []
    accuracy = int(round((dataPoints)**(1/c)))
    size = []
    for i in range(c):
        size.append(accuracy)
    nestledTensor(c,size,innerCoord,constants)
    if onlySurface==True:                                                       # Fungerar någorlunda...
        pops = []
        for i in range(len(xs)):
            upper = False
            lower = False
            for j in range(len(xs)):
                if xs[i] < xs[j] and ys[i] < ys[j] and zs[i] < zs[j]:
                    upper = True
                if xs[i] > xs[j] and ys[i] > ys[j] and zs[i] > zs[j]:
                    lower = True
                if upper == True and lower == True:
                    pops.append(i)
                    break
        pops.reverse()
        for i in pops:
            xs.pop(i)
            ys.pop(i)
            zs.pop(i)
    if sliced==True:
        thickness = conformationMaximumDistance(c,d,α)/20
        maxy = max(ys)
        miny = min(ys)
        pops = []
        for i in range(len(ys)):
            if ys[i] > thickness or ys[i] < -thickness:
                pops.append(i)
        pops.reverse()
        for i in pops:
            xs.pop(i)
            ys.pop(i)
            zs.pop(i)
    fig = pyplot.figure(figsize=(10,8.5))
    ax = fig.gca(projection='3d')
    #ax = fig.add_subplot(111,projection='3d')
    ax.scatter(xs,ys,zs,c=colour,marker='o')
    if sliced==True:
        ax.set_ylim3d(miny,maxy)
    ax.view_init(*rotation)
    pyplot.show()


def conformationMaximumDistance(c,d,α,consoleOut=False):
    αvar = 0
    x = 0
    y = d[0]
    if consoleOut == True:
        print('∆x_1: 0.0')  
        print('∆y_1: '+str(float(y)))  
    for i in range(1,c): # if c=1 → No loop
        if αvar <= -arctan2(x,y):
            αvar += α[i]/2
        else:
            αvar -= α[i]/2
        if consoleOut == True:
            print('∆x_'+str(i+1)+': '+str(d[i]*sin(αvar)))  
            print('∆y_'+str(i+1)+': '+str(d[i]*cos(αvar)))  
        x += d[i]*sin(αvar)
        y += d[i]*cos(αvar)
    return sqrt(x**2+y**2)


def conformationDelta(c,d,α,φ,λ,startCoord,terminalα,terminalλ,terminalCoord):            # Returns a float of the δ-distance for a set of φ
    A_N, b_N = conformationAtomCoordinates(c,d,α,φ,λ,True)
    tα = terminalα
    tλ = terminalλ
    tC = terminalCoord
    A_N[0] += startCoord[0]
    A_N[1] += startCoord[1]
    A_N[2] += startCoord[2]
    δ1 = sqrt((A_N[0]-tC[0])**2+(A_N[1]-tC[1])**2+(A_N[2]-tC[2])**2)
    numerator = b_N[0]*cos(tλ[1])+b_N[1]*sin(tλ[1])+b_N[2]*cos(tλ[0]) # TODO
    denominator = sqrt((b_N[0])**2+(b_N[1])**2+(b_N[2])**2)*sqrt((cos(tλ[1]))**2+(sin(tλ[1]))**2+(cos(tλ[0]))**2)
    δ2 = (arctan2(numerator,denominator)-tα)**2
    #δ2 = (arctan((numerator)/(denominator))-tλ[0])**2                          # Stämmer tλ[0], tλ[0] = φ_T?     PS. Eftersom test uppgav korrekt svar → Troligtvis!
    return δ1 + δ2

# an, bn = conformationAtomCoordinates(4,[1]*4,[carbonAngle]*4,[0,0,0,0],[0,0],True)
# conformationDelta(4,[1]*4,[carbonAngle]*4,[0,0,0,1],[0,0],[0,0,0],carbonAngle,bn,an)


def compactConformationDelta(variables,constants):
    return conformationDelta(constants[0],constants[1],constants[2],variables,constants[3],constants[4],constants[5],constants[6],constants[7])


def conformationDeltaT(c,d,α,φ,λ,startCoord,terminalα,terminalλ,terminalCoord):            # Returns a list of the δ_1-distance and t for a set of φ
    A_N, b_N = conformationAtomCoordinates(c,d,α,φ,λ,True)
    tα = terminalα
    tλ = terminalλ
    tC = terminalCoord
    A_N[0] += startCoord[0]
    A_N[1] += startCoord[1]
    A_N[2] += startCoord[2]
    δ1 = sqrt((A_N[0]-tC[0])**2+(A_N[1]-tC[1])**2+(A_N[2]-tC[2])**2)
    print([sin(tλ[0])*cos(tλ[1]),sin(tλ[0])*sin(tλ[1]),cos(tλ[0])])          # TODO Anger coordinaterna på avstånd 1 i xy-planet, när denna längd egentligen är en projektion av vektorn med längd 1 i xyz-rummet.
    numerator = b_N[0]*sin(tλ[0])*cos(tλ[1])+b_N[1]*sin(tλ[0])*sin(tλ[1])+b_N[2]*cos(tλ[0])
    denominator = sqrt((b_N[0])**2+(b_N[1])**2+(b_N[2])**2)*sqrt((sin(tλ[0])*cos(tλ[1]))**2+(sin(tλ[0])*sin(tλ[1]))**2+(cos(tλ[0]))**2)
    # arctan ← arccos?
    t = abs(arctan2(numerator,denominator)-tα)
    return [δ1,t]


def conformationTensorisation(c,d,α,λ,startCoord,terminalα,terminalλ,terminalCoord,accuracy):     # Returns a tensor with each φ as a variable
    def innerAdd(indexList,const):
        var = indexList.copy()
        for i in range(len(indexList)):                                          # Inget fel på φ_k -> Måste vara tolkningen av φ_k i δ-funktionen
            #var[i] = var[i]*((2*pi)/(accuracy))
            var[i] = (var[i]*(2*pi)/accuracy)-pi
        tensor[tuple(indexList)] = compactConformationDelta(var,const)
    constants = [c,d,α,λ,startCoord,terminalα,terminalλ,terminalCoord]
    size = []
    for i in range(c):
        size.append(accuracy)
    tensor = zeros(size,float)
    nestledTensor(c,size,innerAdd,constants)
    return tensor


def conformationSolver(c,d,α,λ,startCoord,terminalα,terminalλ,terminalCoord,expectedTime=10,proximity='auto'):     # Uses pathfinder and jiggering to find set of φ as a solution
    maxEx = conformationMaximumDistance(c,d,α)
    dist = sqrt((startCoord[0]-terminalCoord[0])**2+(startCoord[1]-terminalCoord[1])**2+(startCoord[2]-terminalCoord[2])**2)
    if maxEx < dist:
        raise Exception("The distance between start and terminal is too big.")
    if not isinstance(proximity,(str,int,float)):
        raise TypeError("'proximity' must be of type string, integer or float.")
    if isinstance(proximity,str):
        if proximity.upper() != 'AUTO' and proximity.upper() != 'BESTFIT':
            raise ValueError("Stringtypes are 'auto' or 'bestFit'.")
    constants = [c,d,α,λ,startCoord,terminalα,terminalλ,terminalCoord]
    mapResolution = int(round((expectedTime/(0.0001*c))**(1/c)))
    localMin = pathfinder(conformationTensorisation(c,d,α,λ,startCoord,terminalα,terminalλ,terminalCoord,mapResolution))
    φlist = []
    for indices in localMin:
        φk = []
        for i in indices:
            φk.append((i*(2*pi)/mapResolution)-pi)
        φlist.append(φk)
    step = pi/mapResolution
    if isinstance(proximity,str):
        if proximity.upper() == 'AUTO':     # 0.07 ← OK, 0.06 ← False
            ε = 0.1
            prox = sqrt((ε+d[c-1]*sin(α[c-1]/2)*(1-cos(step)))**2+(d[c-1]*sin(α[c-1]/2)*sin(step))**2)+(arcsin(sin(α[c-1]/2)*sin(step)))**2
#            prox = 2*d[c-1]*sin(α[c-1]/2)*sin(step)+((2*pi)/mapResolution)   # Fortfarande för liten, α jämför även riktning...
            print('prox - '+str(prox))
            print('ang - '+str(((2*pi)/mapResolution)))
                                                   # Bestäms utifrån avstånd mellan startCoord och terminalCoord samt antalet koner (c)
        elif proximity.upper() == 'BESTFIT':
            prox = 2*maxEx*cos(α[0]/4)
                                                   # Testar flera prox; börjar på givet avstånd tills det att funktionen resulterar i False
    else:
        prox = proximity                     # OPTIMIZE proximity value
    insigCangeThreshold = 1e-50          # sys.float_info.min OPTIMIZE insignificance threshold
#    print('φlist: '+str(φlist))
    solution = jigger(compactConformationDelta,φlist,constants,step,prox,insigCangeThreshold)
    if len(solution) == 0:
        return False
    else:
        return solution


def conformationEnergyCalculator(c,α,φlist):                                    # Calculates the steric hindrance of the calculated solutions
    None
    # Newman projections → Trans, Gauche, Eclipsed, Cis ← Relative conformation energy
    # Possible to find empiric values for specific bonds in proteins?
    # Take into account the resonating peptide "σ"-bond which does not like rotation


carbonAngle = (141*pi)/180 # 360-109.5*2 = 141
alpha = [carbonAngle]*4
phi = [0,0,0,0]
lamb = [0,0]

# conformationVolumePlot(1,[1],[carbonAngle],lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],100,(30,-60),'#363636',sliced=False)
# conformationVolumePlot(2,[1]*2,[carbonAngle]*2,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],2500,(30,-60),'#9871ad',sliced=False)
# conformationVolumePlot(3,[1]*3,[carbonAngle]*3,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],2000,(30,-60),'#29cc9b',sliced=False)
# conformationVolumePlot(4,[1]*4,[carbonAngle]*4,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],1000,(30,-60),'#cc398c',sliced=False)
# conformationVolumePlot(5,[1]*5,[carbonAngle]*5,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],1000,(30,-60),'#5053d9',sliced=False)
# conformationVolumePlot(6,[1]*6,[carbonAngle]*6,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],2000,(30,-60),'#a23325',sliced=False)
# conformationVolumePlot(7,[1]*7,[carbonAngle]*7,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],7000,(30,-60),'#bddc6c',sliced=False)

# matshow(conformationTensorisation(2,[1,1],[carbonAngle]*2,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],50))
# pathfinderChange(conformationTensorisation(2,[1,1],[carbonAngle]*2,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],50))
# voxelMat(conformationTensorisation(3,[1,1,1],[carbonAngle]*3,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],25),sliced=0,minColour=(0,200,180,50),maxColour=(255,200,180,0),compact=False)
# voxelMat(conformationTensorisation(3,[1,1,1],[carbonAngle]*3,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],25),sliced=0,minColour=(0,200,180,255),maxColour=(255,200,180,255),compact=True)

# matshow(pathfinder(conformationTensorisation(2,[1,1],[carbonAngle]*2,lamb,[0,0,0],carbonAngle,[arccos(0.51),arctan2(-0.35,0.78)],[1.33,0.41,0.85],50),6.5))
# voxelMat(pathfinder(conformationTensorisation(3,[1,1,1],[carbonAngle]*3,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],25),0),sliced=0,minColour=(0,200,180,50),maxColour=(255,200,180,0),compact=False)
# voxelMat(conformationTensorisation(3,[1,1,1],[carbonAngle]*3,lamb,[0,0,0],carbonAngle,lamb,[-1,0,-1],50),sliced=0,minColour=(0,200,180,50),maxColour=(255,200,180,0),marker=pathfinder(conformationTensorisation(3,[1,1,1],[carbonAngle]*3,lamb,[0,0,0],lamb,[-1,0,-1],50)),compact=False)
# Då det ej är terminal-konens normalvektor som anges som λ, utan själva resultatvektorn, kan terminal-α anges som 0.

# conformationSolver(2,[1,1],[carbonAngle]*2,lamb,[0,0,0],carbonAngle,[arccos(0.51),arctan2(-0.35,0.78)],[1.33,0.41,0.85],20)


# TODO Kontrollera att rätt terminalλ används utifrån T:s orientering

def plotMaxes(N,d,α,rel=False):
    xs=[]
    ys=[]
    for i in range(1,N+1):
        xs.append(i)
        if rel==True:
            ys.append(conformationMaximumDistance(i,d,α)/sum(d[0:i]))
        else:
            ys.append(conformationMaximumDistance(i,d,α))
    pyplot.plot(xs,ys)
    pyplot.show()




















