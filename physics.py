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
    def div(self,value):
        self.data[0] /= value
        self.data[1] /= value
        return self
    def cross(self,value):
        return (self.data[0] * value.data[1])-(self.data[1]*value.data[0])
    def mag(self):
        return math.sqrt(self.data[0]**2 + self.data[1]**2)

class Matrix2():
    def __init__(self,data):
        self.data = data
    def __mul__(self,value):
        return Vector2([value.data[0]*self.data[0][0] + value.data[1]*self.data[1][0], value.data[0]*self.data[0][1] + value.data[1]*self.data[1][1]])

def normalize(vector):
    mag = math.sqrt(vector.data[0]**2 + vector.data[1]**2)
    vector.data[1] /= mag
    vector.data[0] /= mag
    return vector

def distance(a,b):
    return math.sqrt((a.data[0]-b.data[0])**2 + (a.data[1]-b.data[1])**2)

def sign(x):
    if x >=0:
        return 1
    else:
        return -1

class triangle():
    def __init__(self,points):
        self.points = points
    def toString(self):
        return ""

def averageTriangle(triangle):
    x = 0
    y = 0
    for point in triangle.points:
        x += point.data[0]
        y += point.data[1]
    return Vector2([x/3,y/3])

class collision():
    def __init__(self,a,b,tria,trib,overlap,x,axis):
        self.needshandle = x
        self.a = a
        self.b = b
        self.tria = tria
        self.trib = trib
        self.overlap = overlap
        self.axis = axis

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
    min_axis = None
    min_overlap = 9999
    axes.append(normalize(rotator * (tria.points[0] - tria.points[1])))
    axes.append(normalize(rotator * (tria.points[1] - tria.points[2])))
    axes.append(normalize(rotator * (tria.points[2] - tria.points[0])))
    axes.append(normalize(rotator * (trib.points[0] - trib.points[1])))
    axes.append(normalize(rotator * (trib.points[1] - trib.points[2])))
    axes.append(normalize(rotator * (trib.points[2] - trib.points[0])))
    for item in axes:
        amin, amax = project(tria,item)
        bmin, bmax = project(trib,item)
        if amin > bmin and amin > bmax:
            return True,-1,min_axis
        elif bmin > amin and bmin > amax:
            return True,-1,min_axis
        else:
            overlapA = amax - bmin
            overlapB = bmax - amin
            if overlapA < min_overlap:
                min_overlap = overlapA
                min_axis = item
            if overlapB < min_overlap:
                min_overlap = overlapB
                min_axis = item
    return False,min_overlap,min_axis

def sat(a,b):
    for tria in a.triangles:
        for trib in b.triangles:
            result, overlap,axis =  isGap(tria,trib)
            if not result:
                return collision(a,b,tria,trib,overlap,True,axis)
    return collision(a,b,tria,trib,-1,False,axis)

def goodColor():
    while 1:
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        da = abs(a-b)
        db = abs(b-c)
        dc  = abs(c-a)
        if int((da+db+dc)/3) > 150:
            break
    return a,b,c

rotator = Matrix2([[0,-1],[1,0]])
