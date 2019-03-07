class Vector2():
    def __init__(self,data):
        self.data = data
    def __getitem__(self,key):
        return self.data[key]
    def __add__(self,value):
        return Vector2([self[0]+value[0],self[1]+value[1]])
    def __sub__(self,value):
        return Vector2([self[0]-value[0],self[1]-value[1]])
    def __mul__(self,value):
        return self.dot(value)
    def dot(self,value):
        return self[0]*value[0] + self[1]*value[1]
    def cross(self,value):
        return (self[0] * value[1])-(self[1]*value[0])
    def length(self):
        return math.sqrt(self[0]**2 + self[1]**2)
    def normalize(self):
        mag = self.length()
        return Vector2([self[0]/mag,self[1]/mag])
    def normal(self):
        value = [[0,-1],[1,0]]
        return Vector2([self[0]*value[0][0] + self[1]*value[1][0],self[0]*value[0][1] + self[1]*value[1][1]])
    def mul(self,value):
        return Vector2([self[0]*value,self[1]*value])
    def div(self,value):
        return Vector2([self[0]/value,self[1]/value])
    def toInt(self):
        return [int(self[0]),int(self[1])]
    def rotate(self,rad):
        c = math.cos(rad)
        s = math.sin(rad)
        self[0] = self[0]*c-self[1]*s
        self[1] = self[0]*s+self[1]*c
        return self

#-----------------------------------------------------------------Mat2
class Mat2():
    def __init__(s):
        s.m00, s.m01, s.m10, s.m11 = 0
    def setRad(s,rad):
        c = math.cos(rad)
        s = math.sin(rad)
        s.m00 = c
        s.m01 = -s
        s.m10 = s
        s.m11 = c
    def __mul__(s,vec):
        return Vector2([s.m00 * vec[0] + s.m01 * vec[1], s.m10 * vec[0] + s.m11 * vec[1]])
        
