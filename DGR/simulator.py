import math
import time
import pygame
from Vector import *
from physicsObject import *
from physics import *
pygame.init()

class Simulator:
    def __init__(self):
        self.objects = []
        self.window = pygame.display.set_mode((1000,500))
        pygame.display.set_caption("Boats")
        
    def tick(self):
        for item in self.objects:
            item.tick()
        collisions = []
        for a in self.objects:
            for b in self.objects:
                if a != b:
                    result = sat(a,b)
                    if result[0] == True:
                        collisions.append(collision(a,b,result[1],result[2]))
                        
        for item in collisions:
            item.a.color = (255,0,0)
            item.b.color = (0,0,255)
            #item.translate()
        for item in self.objects:
            item.render(self.window)
        for item in collisions:
            item.render(self.window)
            
    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return False
            clock.tick(20)
            self.window.fill((0,0,0))
            self.tick()
            pygame.display.update()
        

square = [Vector3(100,100,0),Vector3(100,-100,0),Vector3(-100,-100,0),Vector3(-100,100,0)]
rect = [Vector3(100,200,0),Vector3(100,-200,0),Vector3(-100,-200,0),Vector3(-100,200,0)]

x = Simulator()

y = physicsObject(1,square)
y.location = Vector3(540,150,0)
y.rotation = math.pi / 4
#y.velocity = Vector3(-6,0,0)

z = physicsObject(2,rect)
z.location = Vector3(110,250,0)
#z.velocity = Vector3(4,0,0)

x.objects = [y,z]
x.run()

            
        
