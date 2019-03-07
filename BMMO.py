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
        self.inertia = self.mass * 250**2
        self.collideList = []
        
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
                    tempTorque += (event.point-self.location).cross(event.vector)
                    tempVelocity += event.vector.div(self.mass)
                    
            self.velocity += tempVelocity
            self.rotation_velocity += (tempTorque/self.inertia)

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
        for item in self.objects:
            item.tick()
        for a in self.objects:
            for b in self.objects:
                if a != b:
                    collision = sat(a,b)
                    if collision.needshandle == True:
                        item = collision
                        forceVector =item.axis
                        appliedForce = (item.overlap / ( (1/item.a.mass) + (1/item.b.mass)))
                        forceVector.data[0] *= appliedForce
                        forceVector.data[1] *= appliedForce
                        contactPoint = (averageTriangle(item.tria) + averageTriangle(item.trib)).div(2)
                        finala = force(contactPoint,forceVector)
                        forceVectorB = Vector2([forceVector.data[0] * -1,forceVector.data[1] * -1])
                        finalb =  force(contactPoint,forceVectorB)
                        item.a.tick(False)
                        item.b.tick(False)
                        item.a.events.append(finala)
                        item.b.events.append(finalb)
                        item.a.tick(True)
                        item.b.tick(True)
                        
                        #self.collisions.append(collision)
        #for item in self.collisions:
            #direction = normalize(averageTriangle(item.tria) - averageTriangle(item.trib))
                    
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
a.location = Vector2([400,100])
a.velocity = Vector2([0,2])#random.randint(2,3),random.randint(2,3)])
a.rotation_velocity = 0#random.uniform(-0.02,0.02)
a.rotation = 3.14/2
sim.objects.append(a)

b = polygon()
b.location = Vector2([250,500])
b.velocity = Vector2([0,-3])
b.rotation_velocity = 0
b.rotation = 0
b.mass = 20
sim.objects.append(b)

c = polygon()
c.location = Vector2([900,250])
c.velocity = Vector2([-10,1])
c.rotation_velocity = -0.005
c.rotation = 3.14/2
c.mass = 2
sim.objects.append(c)

d = polygon()
d.location = Vector2([550,1000])
d.velocity = Vector2([0,-8])
d.rotation_velocity = 0.005
d.rotation = 0
d.mass = 15
sim.objects.append(d)

sim.run()
                
