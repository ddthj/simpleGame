import math



class material():
    def __init__(s):
        s.density = 0.5
        s.restitution = 0.2

class aabb():
    def __init__(s):
        s.min = Vector2([0,0])
        s.max = Vector2([0,0])
    def collide(a,b):
        if isinstance(b,aabb):
            if a.max[0] < b.min[0] or a.min[0] > b.max[0]:
                return False
            if a.max[1] < b.min[1] or a.min[1] > b.max[1]:
                return False
            return True
        
class collision():
    def __init__(s,a,b,normal,depth):
        s.a = a
        s.b = b
        s.normal = normal
        s.depth = depth

class simulator():
    def __init__(s):
        s.objects = []
    def cvc(a,b):
        x = a.radius + b.radius
        r=x*x
        if r < (a.location[0]+b.location[0])**2 + (a.location[1],b.location[1]):
            d = math.sqrt((a.location[0]-b.location[0])**2 + (a.location[1]-b.location[1])**2)
            normal = b.location - a.location
            depth = r-d
            return True,collision(a,b,normal,depth)
        return False,None
            
        
    def resolveCollision(s,collision):
        a = collision.a
        b = collision.b
        n = collision.normal
        relative_velocity = a.velocity - b.velocity
        velocity_along_normal = 0
        e = min(a.material.restitution, a.material.restitution)
        impulse = -(1 + e) * n
        impulse /= (1 / a.mass) + (1/b.mass)
        force = impulse * n

        a.velocity -= 1 / a.mass * force
        b.velocity -= 1 / b.mass * force
        
        
        
        
