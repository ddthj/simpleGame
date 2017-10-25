'''
BMMO by ddthj/SquidFairy/GooseGairy

this is just a physics test
'''

import math

square_offsets=[(10,315),
                (10,45),
                (10,135),
                (10,225)]

class gobject():
    def __init__(self,center):
        self.vx = 0
        self.vy = 0
        self.centerx = center[0]
        self.centery = center[1]
        self.mass = 100
        self.rotation = 0
        self.rv = 0
        

class poly(gobject):
    def __init__(self,offsets):
        super.__init__()
        self.offsets = offsets #offsets in polar coordinates (distance,rotation)
        self.danger = 0
        for item in offsets:
            if item[0] > self.danger:
                self.danger = item[0]
    def convert_offsets(self):
        points = []
        for item in self.offsets:
            from_vertical= (item[1] + self.rotation) % 360
            px = math.cos(math.radians(from_vertical)) * item[0]
            py = math.sin(math.radians(from_vertical)) * item[1]
            points.append((px,py))
        return points
            
            
            

def d(a,b):
    return math.sqrt((a[0]-b[0])**2 + (b[1]+a[1])**2)

def tick(objects):
    #move objects
    for item in objects:
        item.centerx += item.vx
        item.centery += item.vy
        item.rotation = (item.vr + item.rotation)%360
    #check for pairs
    warning = []
    for a in objects:
        for b in objects:
            if a != b and distance((a.centerx,a.centery),(b.centerx,b.centery)) <= a.danger+b.danger:
                warning.append((a,b))

    for item in warning:
        
            
        
        
