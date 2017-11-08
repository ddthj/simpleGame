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
def s(scale):
    return [(scale+4,315),
            (scale+4,45),
            (scale+4,135),
            (scale+4,225)]
    
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

class me():
    def __init__(self,color,x,y,r,o):
        self.vx = 0
        self.vy = 0
        self.vr = 0
        self.danger = 0
        self.color = color
        self.centerx = x
        self.centery = y
        self.rotation = r
        self.offsets = o
        self.dead = False
    def convert_offsets(self):
        points = []
        for item in self.offsets:
            from_vertical= (item[1] + self.rotation) % 360
            px = (math.cos(math.radians(from_vertical))* item[0])+self.centerx
            py = (math.sin(math.radians(from_vertical))* item[0])+self.centery
            points.append((px,py))
            #print("Point: %s from_vertical: %s new: %s" % (str(str(item[0]) + ","+str(item[1])),str(from_vertical),str(str(px)+" "+str(py))))
        return points
    def test(self):
        return False
    def render(self,scale):
        self.color = [int(self.color[0]/1.2),int(self.color[1]/1.2),int(self.color[2]/1.2)]
        if self.color[0] < 30 and self.color[1] < 30 and self.color[2] < 30:
            self.dead = True
        p = self.convert_offsets()
        for x in range(len(p)):
            if x+1 < len(p):
                pygame.draw.line(window,self.color,p[x],p[x+1],2)
            else:
                pygame.draw.line(window,self.color,p[x],p[0],2)

class gobject():
    def __init__(self,center):
        self.dead = False
        while 1:
            self.f = False
            a = random.randint(0,255)
            b = random.randint(0,255)
            c = random.randint(0,255)
            da = abs(a-b)
            db = abs(b-c)
            dc  = abs(c-a)
            if int((da+db+dc)/3) > 100:
                break
        self.color = [a,b,c]
        self.vx = random.randint(-25,25)
        self.vy = random.randint(-25,25)
        self.vr = 0#random.randint(-14,14)
        self.rotation = 0
        self.centerx = center[0]
        self.centery = center[1]
        self.mass = 100
        self.displacement = center[0] + center[1]
        
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
    def test(self):
        if self.f:
            self.f = False
            return False
            #return me(self.color,self.centerx,self.centery,self.rotation,self.offsets)
        else:
            return False
    def render(self,scale):
        if abs(self.centerx + self.centery) > self.displacement + 10 or abs(self.centerx + self.centery) < self.displacement - 10:
            self.f = True
        if abs(self.centerx + self.centery) > self.displacement + 50 or abs(self.centerx + self.centery) < self.displacement - 50:
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
            self.displacement= self.centerx+self.centery
            
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
        if x+1 <= len(cords):
            a = cords[x]
            b = cords[x+1]
        else:
            a = cords[x]
            b = cords[0]

        if a[1] >= point[1] >= b[1] or a[1] <= point[1] <= b[1]:
            if a[0] >= point[0] and b[0] >= point[0]:
                counts += 1
    if counts % 2 > 0:
        return True
    return False

def tick(objects,scale):
    #move objects
    for a in objects:
        a.centerx += a.vx
        a.centery += a.vy
        a.rotation += a.vr
        a.render(scale)
        Flag = False
        for b in objects:
            if a != b:
                for i in a.convert_offsets():
                    if get_inside(i,b):
                        Flag = True
                        break
        if Flag:
            a.vx *= -1
            a.vy *= -1
    return objects

c = pygame.time.Clock()
objs = []
for x in range(25):

    objs.append(poly((random.randint(0,screenx),random.randint(0,screeny)),s(scale)))
    objs.append(poly((random.randint(0,screenx),random.randint(0,screeny)),s(scale)))

while 1:
    c.tick(20)
    window.fill(white)
    objs = tick(objs,scale)
    new = objs
    objs = []
    for item in new:
        if item.centerx > screenx+100 or item.centerx < -100 or item.centery > screeny+100 or item.centery < -100:
            objs.append(poly((random.randint(0,screenx),random.randint(0,screeny)),s(scale)))
        else:
            if item.dead == False:
                x = item.test()
                if x != False:
                    objs.append(x)
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
