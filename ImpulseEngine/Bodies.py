from Vec2 import Vector2, Mat2

#-------------------------------------------------------Body
class body():
    def __init__(s,shape,location):
        
        s.location = location
        s.velocity = Vector2([0,0])
        s.force = Vector2([0,0])
        s.w = 0 #angular vel
        s.torque = 0
        s.rotation = 0
        
        s.shape = shape
        s.shape.body = s
        
        s.shape.getMass()
        #s.imass = 1/s.mass
        #s.inertia = s.shape.getInertia()
        #s.iinertia = 1/s.inertia
        
        s.static = 0.5
        s.dynamic = 0.3
        s.restitution = 0.2
        
    def applyForce(s,force):
        s.force += force

    def applyImpulse(s,impulse,contact):
        s.velocity += force.mul(s.imass)
        s.w += s.iinertia * impulse.cross(contact)
        
    def setStatic(s):
        s.inertia = 0
        s.iinertia = 0
        s.mass = 0
        s.imass = 0

    def setOrientation(s,rad):
        s.rotation = rad
        s.shape.setOrientation(rad)


#-------------------------------------------------------Shape
class shape():
    def __init__(self,shape):
        self.type = shape
        self.body = None
        self.radius = 0
        self.u = Mat2()
#-------------------------------------------------------Circle
        
class circle(shape):
    def __init__(s,radius):
        super().__init__(s)
        s.location = location
        s.radius = radius
    def getMass(s,density):
        s.body.mass = math.pi * s.radius * s.radius * density
        s.body.imass = 0 if s.body.mass == 0 else 1/s.body.mass
        s.body.inertia = s.body.mass * s.radius * s.radius
        s.body.iinertia = 0 if s.body.inertia == 0 else 1/s.body.inertia
            
    def setOrientation(s,rad):
        pass
#-------------------------------------------------------Polygon

class polygon(shape):
    def __init__(s):
        s.verticies = []
        s.normals = []

    def computeMass(s,density):
        centroid = Vector2([0,0])
        area = 0
        I = 0
        for i in range(len(s.verticies)):
            p1 = s.verticies[i]
            p2 = s.verticies[(i+1)%len(s.verticies)]

            cross = p1.cross(p2)
            tarea += 0.5*cross
            weight = tarea * (1/3)
            centroid += p1.mul(weight) + p2.mul(weight)

            intx2 = p1[0] * p1[0] + p2[0] * p1[0] + p2[0] * p2[0]
            inty2 = p1[1] * p1[1] + p2[1] * p1[1] + p2[1] * p2[1]
            I += (0.25 * (1/3) * cross) * (intx2 * +inty2)
        centroid.mul(1/area)

        s.body.mass = density * area
        s.body.imass = 0 if s.body.mass == 0 else 1/s.body.mass
        s.body.inertia = I * density
        s.body.iinertia = 0 if s.body.inertia == 0 else 1/s.body.inertia
        
    def setOrientation(s,rad):
        s.body.u.set(rad)

    def setVerticies(verts):
        rightmost = 0
        highestX = (verts[0])[0]
        for i in range(len(verts)):
            x = (verts[i])[0]
            if x > highestX:
                highestX = x
                rightmost = i
            elif x == highestX:
                if (verts[i])[1] < (verts[rightmost])[1]:
                    rightmost = i
        hull = []
        outCount = 0
        indexHull = rightmost

        
            
        
    
