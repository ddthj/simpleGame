'''
BMMO by ddthj/SquidFairy/GooseGairy

this is just a physics test
'''

import math
import pygame
import random

pygame.init()
screenx = 1000
screeny = 800
scale = 1
window = pygame.display.set_mode((screenx,screeny),pygame.RESIZABLE)
pygame.display.set_caption('phtest')
white = [255,255,255]
white = [0,0,0]
color = [0,100,250]

square_offsets=[(100,315),
                (100,45),
                (100,135),
                (100,225)]
def r(scale):
    sides = random.randint(3,10)
    c = int(360/sides)
    a = 0
    o = []
    for x in range(sides):
        b = random.randint(1,scale+4)
        a+=c
        o.append((b,a))
    return o

class gobject():
    def __init__(self,center):
        while 1:
            a = random.randint(0,255)
            b = random.randint(0,255)
            c = random.randint(0,255)
            da = abs(a-b)
            db = abs(b-c)
            dc  = abs(c-a)
            if int((da+db+dc)/3) > 100:
                break
        self.color = [a,b,c]
        self.vx = random.randint(-15,15)
        self.vy = random.randint(-15,15)
        self.vr = random.randint(-8,8)
        self.rotation = 0
        self.centerx = center[0]
        self.centery = center[1]
        self.mass = 100
        
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
    def render(self,scale):
        p = self.convert_offsets()
        for x in range(len(p)):
            if x+1 < len(p):
                pygame.draw.line(window,self.color,p[x],p[x+1],2)
            else:
                pygame.draw.line(window,self.color,p[x],p[0],2)            
                   
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

def tick(objects,scale):
    #move objects
    for item in objects:
        item.centerx += item.vx
        item.centery += item.vy
        item.rotation += item.vr
        
        item.render(scale)
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

c = pygame.time.Clock()
objs = []
for x in range(50):
    objs.append(poly((random.randint(0,screenx),random.randint(0,screeny)),r(scale)))
while 1:
    c.tick(20)
    window.fill(white)
    tick(objs,scale)
    new = objs
    objs = []
    for item in new:
        if item.centerx > screenx+100 or item.centerx < -100 or item.centery > screeny+100 or item.centery < -100:
            objs.append(poly((random.randint(0,screenx),random.randint(0,screeny)),r(scale)))
        else:
            objs.append(item)
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scale += 10
            else:
                if scale >= 6:
                    scale -=10
        elif event.type == pygame.VIDEORESIZE:
            
            screenx = event.dict['size'][0]
            screeny = event.dict['size'][1]
            window = pygame.display.set_mode((event.dict['size'][0],int(float(event.dict['size'][0]) * float(3/5))),pygame.RESIZABLE)
            scale = int(screenx/400)**3    
