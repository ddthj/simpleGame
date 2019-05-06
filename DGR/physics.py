import math
import pygame
from Vector import *

class collision:
    def __init__(self,a,b,axis,gap):
        self.a = a
        self.b = b
        self.axis = axis
        self.gap = gap
        
    def translate(self):
        total = self.a.mass + self.b.mass
        self.a.location -= (self.axis.normal * (self.gap * self.a.mass/total))
        self.b.location += (self.axis.normal * (self.gap * self.b.mass/total))
        
    def get_manifold(self):
        pass
        


def P(start,end,point):
    return (end[0]-start[0])*(point[1]-start[1]) - (end[1]-start[1])*(point[0]-start[0])

def get_axes(points):
    axes = []
    for i in range(len(points)):
        if i < len(points) - 1:
            axes.append(Edge(points[i+1],points[i]))
        else:
            axes.append(Edge(points[0],points[i]))
    return axes
    
def sat(a,b):
    apoints = a.points
    bpoints = b.points
    axes = get_axes(apoints) + get_axes(bpoints)
    min_axis = axes[0]
    min_over = 9999
    for axis in axes:
        ap = sorted([axis.normal.dot(point) for point in apoints])
        bp = sorted([axis.normal.dot(point) for point in bpoints])
        if ap[0] > bp[-1] or bp[0] > ap[-1]:
            return False,axis,0
        else:
            aover = ap[-1]-bp[0]
            bover = bp[-1] - ap[0]
            if aover < min_over:
                min_over = aover
                min_axis = axis
            if bover < min_over:
                min_over = bover
                min_axis = axis
    return True,min_axis,min_over
