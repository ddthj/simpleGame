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
        for event in self.events:
            if isinstance(event,force):
                pass
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

class collision():
    def __init__(self,a,b):
        self.a = a
        self.b = b

class force():
    def __init__(self,point,magnitude,direction):
        self.point = point
        self.magnitude = magnitude
        self.direction = direction

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
                    self.collisions.append(collision(a,b))
                    
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

sim = simulator()
for x in range(2):
    b = polygon()
    b.location = Vector2([random.randint(0,screen_width),random.randint(0,screen_height)])
    b.velocity = Vector2([random.randint(-3,3),random.randint(-3,3)])
    b.rotation_velocity = random.uniform(-0.2,0.2)
    sim.objects.append(b)
sim.run()
                
