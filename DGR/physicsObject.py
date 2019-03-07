import math
import pygame
from Vector import *

class physicsObject:
    def __init__(self,name,shape):
        self.location = Vector3(0,0,0)
        self.rotation = math.pi/2
        
        self.velocity = Vector3(0,0,0)
        self.rvelocity = 0

        self.offsets = shape
        self.mass = 100
        self.moment = self.mass **2
        self.name = name
        self.color = (255,255,255)
        
    def points(self):
        delta = RotationMatrix2D(self.rotation)
        return [self.location + delta.dot(point) for point in self.offsets]

    def tick(self):
        self.location += self.velocity
        self.rotation += self.rvelocity

    def render(self,window):
        points = self.points()
        for i in range(len(points)):
            if i < len(points) - 1:
                pygame.draw.line(window,self.color,points[i].render(), points[i+1].render(), 2)
            else:
                pygame.draw.line(window,self.color,points[i].render(), points[0].render(), 2)
        
            
        
