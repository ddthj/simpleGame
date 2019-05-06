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
        self.points = self.get_points()
        self.mass = 100
        self.moment = self.mass **2
        self.name = name
        self.color = (255,255,255)
        
    def get_points(self):
        delta = RotationMatrix2D(self.rotation)
        return [self.location + delta.dot(point) for point in self.offsets]

    def tick(self):
        self.location += self.velocity
        self.rotation += self.rvelocity
        self.points = self.get_points()

    def render(self,window):
        for i in range(len(self.points)):
            if i < len(self.points) - 1:
                pygame.draw.line(window,self.color,self.points[i].render(), self.points[i+1].render(), 2)
            else:
                pygame.draw.line(window,self.color,self.points[i].render(), self.points[0].render(), 2)
        
            
        
