import math
import pygame
from physics import *

pygame.init()

screen_width = 1000
screen_height = 562
window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("BMMO")

black = (0,0,0)

class polygon():
    def __init__(self):
        self.location = Vector2([0,0])
        self.velocity = Vector2([0,0])
        self.rotation = math.pi/2
        self.rotation_velocity = 0.1
        self.offsets= [Vector2([0,200]), Vector2([50,150]), Vector2([50,-150]), Vector2([-50,-150]), Vector2([-50,150])]
        self.triangles = self.makeTriangles()
        self.color = goodColor()
        self.events = []
        self.mass = 10
        
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
            tempVelocity = Vector2([0,0])
            tempTorque = 0
            for event in self.events:
                if isinstance(event,force):
                    tempVelocity += event.vector
            self.velocity += tempVelocity

            
            self.location += self.velocity
            self.rotation += self.rotation_velocity
            self.events = []
        else:
            self.location -= self.velocity
            self.rotation -= self.rotation_velocity
        self.triangles = self.makeTriangles()

    def render(self):
        for item in self.triangles:
            pygame.draw.line(window,self.color,item.points[0].data,item.points[1].data,1)
            pygame.draw.line(window,self.color,item.points[1].data,item.points[2].data,1)
            pygame.draw.line(window,self.color,item.points[2].data,item.points[0].data,1)

class force():
    def __init__(self,point,vector):
        self.point = point
        self.vector = vector

class simulator():
    def __init__(self):
        self.objects = []
        self.collisions = []

    def tick(self):
        self.collisions = []
        for item in self.objects:
            item.tick()
        for a in self.objects:
            for b in self.objects:
                if a != b:
                    collision = sat(a,b)
                    if collision.needshandle == True:
                        self.collisions.append(collision)
        for item in self.collisions:
            forceVector = normalize(averageTriangle(item.tria) - averageTriangle(item.trib))
            appliedForce = (item.overlap / ( (1/item.a.mass) + (1/item.b.mass)))/50
            forceVector.data[0] *= appliedForce
            forceVector.data[1] *= appliedForce
            finala = force(item.a.location,forceVector)
            forceVectorB = Vector2([forceVector.data[0] * -1,forceVector.data[1] * -1])
            finalb =  force(item.b.location,forceVectorB)

            item.a.tick(False)
            item.b.tick(False)
            item.a.events.append(finala)
            item.b.events.append(finalb)
            
            item.a.tick(True)
            item.b.tick(True)

        
                    
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
            clock.tick(20)
            self.tick()
            self.render()

sim = simulator()
a = polygon()
a.location = Vector2([0,0])
a.velocity = Vector2([random.randint(2,3),random.randint(2,3)])
arotation_velocity = random.uniform(-0.02,0.02)
sim.objects.append(a)

b = polygon()
b.location = Vector2([screen_width,screen_height])
b.velocity = Vector2([random.randint(-3,-2),random.randint(-3,-2)])
b.rotation_velocity = random.uniform(-0.02,0.02)
sim.objects.append(b)
sim.run()
                
