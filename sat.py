import math
import pygame
import random

pygame.init()
screenx = 1000
screeny = 800

window = pygame.display.set_mode((screenx,screeny),pygame.RESIZABLE)
pygame.display.set_caption('SAT TEST')
white = [0,0,0]
color = [0,100,250]

square_offsets=[(100,315),
                (100,45),
                (100,135),
                (100,225)]
wat = [(80,0),
       (80,60),
       (80,120),
       (80,180),
       (80,240),
       (80,300),
    ]
def d(a,b):
    return math.sqrt((a[0]-b[0])**2 + (b[1]+a[1])**2)

def goodColor():
    while 1:
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        da = abs(a-b)
        db = abs(b-c)
        dc  = abs(c-a)
        if int((da+db+dc)/3) > 100:
            break
    return a,b,c

class gobject():
    def __init__(self,center):
        self.color = goodColor()
        self.vx = 0
        self.vy = 0
        self.vr = 0
        self.rotation = 0
        self.centerx = center[0]
        self.centery = center[1]
        self.mass = 100
    def tick(self):
        self.centerx += self.vx
        self.centery += self.vy
        self.rotation += self.vr

class poly(gobject):
    def __init__(self,center,offsets):
        super().__init__(center)
        self.offsets = offsets #offsets in polar coordinates (distance,rotation)
        self.danger = 0 #farthest offset
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
        return points
    
    def render(self):            
        p = self.convert_offsets()
        for x in range(len(p)):
            if x+1 < len(p):
                pygame.draw.line(window,self.color,p[x],p[x+1],1)
            else:
                pygame.draw.line(window,self.color,p[x],p[0],1)

def perp(a,b):
    run = float(a[0] - b[0])
    rise = float(a[1] - b[1])
    return -rise,run

def dot(a,b):
    return (a[0] * b[0]) + (a[1] * b[1])

def get_axes(a):
    temp = []
    lx = len(a.offsets)
    poffsets = a.convert_offsets()
    for x in range(0,lx):
        pa = poffsets[x]
        if x+1 < lx:
            pb = poffsets[x+1]
        else:
            pb = poffsets[0]
        temp.append(perp(pa,pb))
    return temp

def project(a,b): #returns the min and max projection on the axis
    poffsets = a.convert_offsets()
    mi = dot(poffsets[0],b)
    ma = mi
    for item in poffsets:
        p = dot(item,b)
        if p > ma:
            ma = p
        elif p < mi:
            mi = p
    return mi,ma

def overlap(a,b):
    alen = abs(a[0] - a[1])
    blen = abs(b[0] - b[1])
    tlen = abs(a[0] - b[1])
    print(blen)
    overlap_dis = (tlen - (alen+blen))/2
    if b[0] >= a[0] and b[0] <= a[1]:
        return True,overlap_dis
    elif b[1] >= a[0] and b[1] <= a[1]:
        return True,overlap_dis
    elif a[0] >= b[0] and a[0] <= b[1]:
        return True,overlap_dis
    elif a[1] >= b[0] and a[1] <= b[1]:
        return True,overlap_dis
    return False,overlap_dis
 
def satTest(a,b):
    axes = get_axes(a)
    min_overlap_dis = 9999999
    min_overlap_axis = axes[0]
    for item in axes:
        pa = project(a,item)
        pb = project(b,item)
        if overlap(pa,pb)[0] == False:
            return False
        else:
            #print(overlap(pa,pb)[1])
            pygame.draw.line(window,a.color,((a.centerx - 100),(a.centery - 100)), ((a.centerx + 100)*item[0],(a.centery + 100)*item[1]),1)
    axes = get_axes(b)
    for item in axes:
        pa = project(a,item)
        pb = project(b,item)
        if overlap(pa,pb)[0] == False:
            return False
        else:
            #print(overlap(pa,pb)[1])
            pygame.draw.line(window,b.color,((b.centerx - 100),(b.centery - 100)), ((b.centerx + 100)*item[0],(b.centery + 100)*item[1]),1)
    return True

class sim():
    def __init__(self):
        self.obj = []
        a = poly((0,0),square_offsets)
        b = poly((800,800),square_offsets)
        c = poly((800,0),wat)
        d = poly((0,200),wat)
        d.vx = 12
        d.vy = 2
        c.vx = -10
        c.vy = 9
        c.vr = 4
        a.vx = 8
        a.vy = 8
        b.vx = -8
        b.vy = -8
        b.vr = 2
        a.vr = 0
        self.obj.append(a)
        self.obj.append(b)
        #self.obj.append(c)
        #self.obj.append(d)
        self.run()
    def tick(self):
        for item in self.obj:
            item.tick()
            item.render()
            for other in self.obj:
                if item != other:
                    result = satTest(item,other)
                    #print(result)
    def run(self):
        clock = pygame.time.Clock()
        good = False
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        good = True
            clock.tick(20)
            window.fill(white)
            if good:
                self.tick()
                good = False
                pygame.display.update()
            

sim = sim()
