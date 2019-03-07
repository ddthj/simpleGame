import math
import pygame
from Vector import *

class collision:
    def __init__(self,a,b,axis,gap):
        self.a = a
        self.b = b
        self.name = a.name + b.name
        self.axis = axis
        self.reference = None
        self.incident = None
        self.ap = None
        self.bp = None
        self.getEdges()
        self.gap = gap
        self.renderPoints = self.getManifold()
        
    def translate(self):
        total = self.a.mass + self.b.mass
        self.a.location -= (self.axis.normal * (self.gap * self.a.mass/total))
        self.b.location += (self.axis.normal * (self.gap * self.b.mass/total))
    def getManifold(self):
        s1 = self.reference.direction.dot(self.reference.start)
        t1 = self.clip(self.incident,self.reference.direction,s1)
        if len(t1) < 2:
            print("heck")
        else:
            e1 = Edge(t1[0],t1[1])
            points2 = self.clip(e1,-1 * self.reference.direction,-1 * s1)
            return points2
        
    def getEdges(self):
        a,ap = self.best(self.a.points(),self.axis.normal)
        b,bp = self.best(self.b.points(),self.axis.normal * -1)
        self.ap = ap
        self.bp = bp
        if abs(a.direction.dot(self.axis.normal)) <= abs(b.direction.dot(self.axis.normal)):
            self.reference = a
            self.incident = b
        else:
            self.reference = b
            self.incident = a
        
    def best(self,points,axis):
        p = [axis.dot(point) for point in points]
        deepest = 0
        for i in range(len(p)):
            if p[i] > p[deepest]:
                deepest = i
        p0 = points[deepest-1 % len(p)]
        p1 = points[deepest]
        p2 = points[deepest+1 % len(p)]
        if (p1-p0).dot(axis) <= (p1-p2).dot(axis):
            return Edge(p0,p1),points[deepest]
        else:
            return Edge(p1,p2),points[deepest]
        
    def clip(self,edge,ref,dist):
        temp = []
        d1 = edge.start.dot(ref)
        d2 = edge.end.dot(ref)
        if d1 > 0:
            temp.append(edge.start)
        if d2 > 0:
            temp.append(edge.end)
        if d1 * d2 < 0:
            m = d1/(d1-d2)
            temp.append((edge.direction*m)+edge.start)
        return temp
        
        
    def render(self,window):
        pygame.draw.line(window,(0,255,255),self.reference.start.render(),self.reference.end.render(),2)
        pygame.draw.line(window,(255,255,0),self.incident.start.render(),self.incident.end.render(),2)
        pygame.draw.circle(window,(255,255,255),self.ap.render(),5)
        pygame.draw.circle(window,(255,255,255),self.bp.render(),5)
        for item in self.renderPoints:
            pygame.draw.circle(window,(255,0,255),item.render(),5)
        
        

def get_axes(points):
    axes = []
    for i in range(len(points)):
        if i < len(points) - 1:
            axes.append(Edge(points[i+1],points[i]))
        else:
            axes.append(Edge(points[0],points[i]))
    return axes
    
def sat(a,b):
    apoints = a.points()
    bpoints = b.points()
    axes = get_axes(apoints) + get_axes(bpoints)
    min_axis = axes[0]
    min_over = 9999
    for axis in axes:
        ap = sorted([axis.normal.dot(point) for point in apoints])
        bp = sorted([axis.normal.dot(point) for point in bpoints])
        if ap[0] > bp[-1] or bp[0] > ap[-1]:
            return False,axis,0
        else:
            aover = ap[-1]-bp[0]
            bover = bp[-1] - ap[0]
            if aover < min_over:
                min_over = aover
                min_axis = axis
            if bover < min_over:
                min_over = bover
                min_axis = axis
    return True,min_axis,min_over
                
        
    
    
    
    
        
