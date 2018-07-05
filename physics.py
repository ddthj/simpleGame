import math
import random

class Vector2():
    def __init__(self,data):
        self.data = data
    def __add__(self,value):
        return Vector2([self.data[0]+value.data[0],self.data[1]+value.data[1]])
    def __sub__(self,value):
        return Vector2([self.data[0]-value.data[0],self.data[1]-value.data[1]])
    def __mul__(self,value):
        return self.data[0]*value.data[0] + self.data[1]*value.data[1]

class Matrix2():
    def __init__(self,data):
        self.data = data
    def __mul__(self,value):
        return Vector2([value.data[0]*self.data[0][0] + value.data[1]*self.data[1][0], value.data[0]*self.data[0][1] + value.data[1]*self.data[1][1]])

class triangle():
    def __init__(self,points):
        self.points = points
    def toString(self):
        return 

def averageTriangle(triangle):
    x = 0
    y = 0
    for point in triangle:
        x += point.data[0]
        y+= point.data[1]
    return (x/3,y/3)

def project(triangle,axis):
    maxPoint = triangle.points[0] * axis
    minPoint = triangle.points[0] * axis
    for item in triangle.points:
        if item * axis > maxPoint:
            maxPoint = item * axis
        if item * axis < minPoint:
            minPoint = item * axis
    return minPoint,maxPoint

def isGap(tria,trib):
    axes = []            
    axes.append(rotator * (tria.points[0] - tria.points[1]))
    axes.append(rotator * (tria.points[1] - tria.points[2]))
    axes.append(rotator * (tria.points[2] - tria.points[0]))
    axes.append(rotator * (trib.points[0] - trib.points[1]))
    axes.append(rotator * (trib.points[1] - trib.points[2]))
    axes.append(rotator * (trib.points[2] - trib.points[0]))
    for item in axes:
        amin, amax = project(tria,item)
        bmin, bmax = project(trib,item)
        if amin > bmin and amin > bmax:
            return True
        if bmin > amin and bmin > amax:
            return True
    return False

def sat(a,b):
    for tria in a.triangles:
        for trib in b.triangles:
            if not isGap(tria,trib):
                return True
    return False

def goodColor():
    while 1:
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        da = abs(a-b)
        db = abs(b-c)
        dc  = abs(c-a)
        if int((da+db+dc)/3) > 100:
            break
    return a,b,c

rotator = Matrix2([[0,-1],[1,0]])
