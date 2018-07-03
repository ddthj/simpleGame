import math
import pygame
import random

pygame.init()

screen_width = 1000
screen_height = 562
window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("BMMO")

black = (0,0,0)


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

class polygon():
    def __init__(self):
        self.location = Vector2([0,0])
        self.velocity = Vector2([0,0])
        self.rotation = math.pi/2
        self.rotation_velocity = 0.1
        self.offsets= [Vector2([0,200]), Vector2([50,150]), Vector2([50,-150]), Vector2([-50,-150]), Vector2([-50,150])]
        self.triangles = self.makeTriangles()
        self.color = goodColor()
        
    def makeTriangles(self):
        temp = []
        for x in range(len(self.offsets)):
            if x+1 < len(self.offsets):
                temp.append(triangle([self.location,self.toPoint(self.offsets[x]),self.toPoint(self.offsets[x+1])]))
            else:
                temp.append(triangle([self.location,self.toPoint(self.offsets[x]),self.toPoint(self.offsets[0])]))
        return temp

    def toPoint(self,offset):

        c = math.cos(self.rotation)
        s = math.sin(self.rotation)

        x = self.location.data[0] + c * offset.data[0] - s * offset.data[1]
        y = self.location.data[1] + s * offset.data[0] + c * offset.data[1]
        return Vector2([x,y])

    def tick(self,forward = True):
        if forward:
            self.location += self.velocity
            self.rotation += self.rotation_velocity
        else:
            self.location -= self.velocity
            self.rotation -= self.rotation_velocity

        self.triangles = self.makeTriangles()

    def render(self):
        for item in self.triangles:
            pygame.draw.line(window,self.color,item.points[0].data,item.points[1].data,1)
            pygame.draw.line(window,self.color,item.points[1].data,item.points[2].data,1)
            pygame.draw.line(window,self.color,item.points[2].data,item.points[0].data,1)

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

class simulator():
    def __init__(self):
        self.objects = []

    def tick(self):
        for item in self.objects:
            item.tick()
        for a in self.objects:
            for b in self.objects:
                if a != b:
                    print(sat(a,b))
                    
    def render(self):
        window.fill(black)
        for item in self.objects:
            item.render()
        pygame.display.update()
    def run(self):
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        pygame.quit()
                        exit
            clock.tick(5)
            self.tick()
            self.render()


rotator = Matrix2([[0,-1],[1,0]])
sim = simulator()
for x in range(2):
    b = polygon()
    b.location = Vector2([random.randint(0,screen_width),random.randint(0,screen_height)])
    b.velocity = Vector2([random.randint(-3,3),random.randint(-3,3)])
    b.rotation_velocity = random.uniform(-0.2,0.2)
    sim.objects.append(b)
sim.run()
                
