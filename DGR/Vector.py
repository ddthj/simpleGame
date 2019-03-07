import math

class RotationMatrix2D:
    def __init__(self,theta):
        self.data = [[math.cos(theta),-math.sin(theta)],[math.sin(theta), math.cos(theta)]]
    def dot(self,vector):
        return Vector3(self.data[0][0]*vector[0] + self.data[1][0]*vector[1], self.data[0][1]*vector[0] + self.data[1][1]*vector[1], 0)
    
class Vector3:
    def __init__(self, *args):
        self.data = args[0] if isinstance(args[0],list) else [x for x in args]
    def __getitem__(self,key):
        return self.data[key]
    def __str__(self):
        return str(self.data)
    def __add__(self,value):
        return Vector3(self[0]+value[0], self[1]+value[1], self[2]+value[2])
    def __sub__(self,value):
        return Vector3(self[0]-value[0],self[1]-value[1],self[2]-value[2])
    def __mul__(self,value):
        return Vector3(self[0]*value, self[1]*value, self[2]*value)
    __rmul__ = __mul__
    def __eq__(self,vector):
        if self[0] == vector[0] and self[1] == vector[1] and self[2] == vector[2]:
            return True
        return False
    def __div__(self,value):
        return Vector3(self[0]/value, self[1]/value, self[2]/value)
    def compare(self,value):
        x = 1 if self[0] == value[0] else 0
        if self[1] == value[1]: x += 1 
        if self[2] == value[2]: x += 1 
        return x
    def magnitude(self):
        return math.sqrt((self[0]*self[0]) + (self[1] * self[1]) + (self[2]* self[2]))
    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return Vector3(self[0]/mag, self[1]/mag, self[2]/mag)
        else:
            return Vector3(0,0,0)
    def dot(self,value):
        return self[0]*value[0] + self[1]*value[1] + self[2]*value[2]
    def cross(self,value):
        return Vector3((self[1]*value[2]) - (self[2]*value[1]),(self[2]*value[0]) - (self[0]*value[2]),(self[0]*value[1]) - (self[1]*value[0]))
    def flatten(self):
        return Vector3(self[0],self[1],0)
    def render(self):
        return (int(self[0]),int(self[1]))
    def angle(self,vector):
        return math.atan2(vector[1],vector[0]) - math.atan2(self[1],self[0])

class Edge:
    def __init__(self,start,end):
        self.start = start
        self.end = end
        self.relative = self.end - self.start
        self.direction = self.relative.normalize()
        self.normal = self.direction.cross(rot)
    def max(self):
        if self.start.dot(self.direction) > self.end.dot(self.direction):
            return self.start
        else:
            return self.end

rot = Vector3(0,0,1)
