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
        x = self.location.data[0] + offset.data[0]*math.cos(self.rotation%(2*math.pi))
        y = self.location.data[1] + offset.data[1]*math.sin(self.rotation%(2*math.pi))
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
            
class simulator():
    def __init__(self):
        self.objects = []

    def tick(self):
        for item in self.objects:
            item.tick()
    def render(self):
        window.fill(black)
        for item in self.objects:
            item.render()
        pygame.display.update()
    def run(self):
        clock = pygame.time.Clock()
        while 1:
            events = pygame.event.get()
            clock.tick(20)
            self.tick()
            self.render()

sim = simulator()
b = polygon()
b.location = Vector2([screen_width/2,screen_height/2])
b.velocity = Vector2([1,2])
sim.objects.append(b)
sim.run()
                
