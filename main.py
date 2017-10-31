'''
BMMO by ddthj/SquidFairy/GooseGairy

this is just a physics test
'''

import math
import pygame
import random

pygame.init()
window = pygame.display.set_mode((1000,800),pygame.RESIZABLE)
pygame.display.set_caption('phtest')
white = [255,255,255]
color = [0,100,250]

square_offsets=[(100,315),
                (100,45),
                (100,135),
                (100,225)]

class gobject():
    def __init__(self,center):
        self.vx = 0
        self.vy = 0
        self.centerx = center[0]
        self.centery = center[1]
        self.mass = 100
        self.rotation = 1
        self.vr = 45
        
class poly(gobject):
    def __init__(self,center,offsets):
        super().__init__(center)
        self.offsets = offsets #offsets in polar coordinates (distance,rotation)
        self.danger = 0
        for item in offsets:
            if item[0] > self.danger:
                self.danger = item[0]
    def convert_offsets(self):
        points = []
        for item in self.offsets:
            from_vertical= (item[1] + self.rotation) % 360
            px = (math.cos(math.radians(from_vertical))* item[0])+self.centerx
            py = (math.sin(math.radians(from_vertical))* item[0])+self.centery
            points.append((px,py))
            #print("Point: %s from_vertical: %s new: %s" % (str(str(item[0]) + ","+str(item[1])),str(from_vertical),str(str(px)+" "+str(py))))
            
        return points
    def render(self):
        p = self.convert_offsets()
        for x in range(len(p)):
            if x+1 < len(p):
                pygame.draw.line(window,color,p[x],p[x+1],1)
            else:
                pygame.draw.line(window,color,p[x],p[0],1)            
                   
def d(a,b):
    return math.sqrt((a[0]-b[0])**2 + (b[1]+a[1])**2)

def get_inside(point,obj):
    cords = obj.convert_offsets()
    counts = 0
    for x in range(len(cords)-1):
        if x+1 < len(cords):
            a = cords[x]
            b = cords[x+1]
        else:
            a = cords[x]
            b = cords[0]

        if a[1] > point[1] > b[1] or a[1] < point[1] < b[1]:
            counts += 1
    if counts % 2 > 0:
        return True
    return False

def tick(objects):
    #move objects
    for item in objects:
        item.centerx += item.vx
        item.centery += item.vy
        item.rotation += random.randint(1,8)
        item.vx += random.randint(-2,2)
        item.vy += random.randint(-2,2)
        
        item.render()
    #check for pairs
    warning = []
    for a in objects:
        for b in objects:
            if a != b and d((a.centerx,a.centery),(b.centerx,b.centery)) <= a.danger+b.danger:
                warning.append((a,b))

    for item in warning:
        a = item[0]
        b = item[1]
        for item in a.convert_offsets():
            if get_inside(item,b):
                pass
                #print("c")
        for item in b.convert_offsets():
            if get_inside(item,a):
                pass
                #print("c")

def randomP():
    pass
c = pygame.time.Clock()
objs = []
screenx = 1000
screeny = 800
while 1:
    r_offsets=[(random.randint(10,150),315),
                (random.randint(10,150),45),
                (random.randint(10,150),135),
                (random.randint(10,150),225)]
    c.tick(20)
    window.fill(white)
    tick(objs)
    new = objs
    objs = []
    for item in new:
        if item.centerx > screenx+100 or item.centerx < -100 or item.centery > screeny+100 or item.centery < -100:
            pass
        else:
            objs.append(item)

    
    if len(objs) < random.randint(10,25):
        if random.randint(0,10) % 2 == 0:
            objs.append(poly((random.randint(0,screenx),random.randint(0,screeny)),square_offsets))
        else:
            objs.append(poly((random.randint(0,screenx),random.randint(0,screeny)),r_offsets))
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.VIDEORESIZE:
            screenx = event.dict['size'][0]
            screeny = event.dict['size'][1]
            window = pygame.display.set_mode((event.dict['size'][0],int(float(event.dict['size'][0]) * float(3/5))),pygame.RESIZABLE)
    
