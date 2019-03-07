import math
import pygame
import random

"""
Very early physics simulator prototype

ddthj V1
"""

random.seed(12)
pygame.init()

screen_width = 1000
screen_height = 562
window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("BMMO")

black = (255,255,255)
axesColor = (255,170,0)
aa = (0,255,0)
bb = (0,200,0)
cc = (0,0,255)
dd = (0,0,200)
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

def getAxes(a):
    axes = []
    for i in range(0,len(a.points)):
        if i < len(a.points)-1:
            axes.append((a.points[i]-a.points[i+1]).normal().normalize())
        else:
            axes.append((a.points[i]-a.points[0]).normal().normalize())
    return axes

def project(a,axis):
    a_min = 9999
    a_max = -9999
    for point in a.points:
        p = axis.dot(point)
        if p > a_max:
            a_max = p
        elif p < a_min:
            a_min = p
    return a_min, a_max
        

def sat(a,b):
    axes = getAxes(a) + getAxes(b)
    for axis in axes:
        a_min, a_max = project(a,axis)
        b_min, b_max = project(b,axis)
        
        
        '''
        loc = (a.location + b.location).div(2)
        amp = loc + axis.mul(a_max)
        amip = loc+ axis.mul(a_min)
        bmp = loc+ axis.mul(b_max)
        bmip = loc+ axis.mul(b_min)
        if a_min < b_min:
            minn = amip
        else:
            minn = bmip
        if a_max > b_max:
            maxx = amp
        else:
            maxx = bmp
        pygame.draw.line(window,axesColor,minn.data,maxx.data,2)
        pygame.draw.circle(window,aa,amp.toInt(),4,0)
        pygame.draw.circle(window,bb,amip.toInt(),4,0)
        pygame.draw.circle(window,cc,bmp.toInt(),4,0)
        pygame.draw.circle(window,dd,bmip.toInt(),4,0)
        '''
    return False

class Vector2():
    def __init__(self,data):
        self.data = data
    def __add__(self,value):
        return Vector2([self.data[0]+value.data[0],self.data[1]+value.data[1]])
    def __sub__(self,value):
        return Vector2([self.data[0]-value.data[0],self.data[1]-value.data[1]])
    def __mul__(self,value):
        return self.dot(value)
    def dot(self,value):
        return self.data[0]*value.data[0] + self.data[1]*value.data[1]
    def cross(self,value):
        return (self.data[0] * value.data[1])-(self.data[1]*value.data[0])
    def normalize(self):
        mag = math.sqrt(self.data[0]**2 + self.data[1]**2)
        return Vector2([self.data[0]/mag,self.data[1]/mag])
    def normal(self):
        value = [[0,-1],[1,0]]
        return Vector2([self.data[0]*value[0][0] + self.data[1]*value[1][0],self.data[0]*value[0][1] + self.data[1]*value[1][1]])
    def mul(self,value):
        return Vector2([self.data[0]*value,self.data[1]*value])
    def div(self,value):
        return Vector2([self.data[0]/value,self.data[1]/value])
    def toInt(self):
        return [int(self.data[0]),int(self.data[1])]
        
def d(a,b):
    return math.sqrt((a.data[0]-b.data[0])**2 + (a.data[1]-b.data[1])**2)

def sign(x):
    if x >=0:
        return 1
    else:
        return -1

class force():
    def __init__(self,point,vector):
        self.point = point
        self.vector = vector

class collision():
    def __init__(self,a,b,overlap,x,axis):
        self.needshandle = x
        self.a = a
        self.b = b
        self.overlap = overlap
        self.axis = axis   
        

class polygon():
    def __init__(self):
        self.location = Vector2([0,0])
        self.velocity = Vector2([0,0])
        self.rotation = math.pi/2
        self.rotation_velocity = 0
        self.offsets = [[-25,25],[25,25],[25,-25],[-25,-25]]
        self.points = self.updatePoints()

        self.mass = 20
        self.moment = 300**2

        self.events = []

        #debug
        self.color = goodColor()
        
    def updatePoints(self):
        temp = []
        for offset in self.offsets:
            c = math.cos(self.rotation)
            s = math.sin(self.rotation)
            x = self.location.data[0] + c * offset[0] - s * offset[1]
            y = self.location.data[1] + s * offset[0] + c * offset[1]
            temp.append(Vector2([x,y]))
        self.points = temp

    def tick(self,t): #may change to physicsTick that only handles physics events
        tempVelocity = Vector2([0,0])
        tempTorque = 0
        for event in self.events:
            if isinstance(event,force):
                tempVelocity += event.vector.div(self.mass)
                tempTorque += (self.location-event.point).cross(event.vector)
                
        self.velocity += tempVelocity
        self.rotation_velocity += tempTorque/self.moment
        self.location += self.velocity.mul(t)
        self.rotation += self.rotation_velocity
        self.events = []

        self.updatePoints()

    def render(self):
        for point in self.points:
            pygame.draw.circle(window,self.color,point.toInt(),4,0)
        for i in range(0,len(self.points)):
            if i <len(self.points)-1:
                pygame.draw.line(window,self.color,self.points[i].data,self.points[i+1].data,2)
            else:
                pygame.draw.line(window,self.color,self.points[i].data,self.points[0].data,2)

class simulator():
    def __init__(self):
        self.objects = []

    def run(self):
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        pygame.quit()
                        exit
            clock.tick(20)
            self.tick()
            self.render()
            
        
    def render(self):
        for item in self.objects:
            item.render()
        pygame.display.update()
        window.fill(black)

    def tick(self):
        pass
            
sim = simulator()
a = polygon()
a.location = Vector2([350,300])
a.velocity = Vector2([0,0])
a.rotation_velocity = 0.05
a.rotation = 3.14/2
a.updatePoints()
sim.objects.append(a)

b = polygon()
b.location = Vector2([305,850])
b.velocity = Vector2([0,-1])
b.rotation_velocity = 0
b.rotation = 0.1
b.mass = 20
b.updatePoints()
sim.objects.append(b)

sim.run()
