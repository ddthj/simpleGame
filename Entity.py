from LinAlg import Vector, Matrix3
from Shapes import circle
from math import pi


def find_mass_inertia(entity):
    mass = inertia = 0
    if entity.density == 0:
        return 0, 0
    if len(entity.shape) == 1:
        radius = entity.radius
        mass = pi * radius * radius * entity.density
        inertia = pi * 0.5 * radius * radius * radius * radius
    else:
        for i in range(len(entity.shape)):
            face = (entity.shape[i - 1], entity.shape[i])
            face_mass = entity.density * 0.5 * abs(face[0].cross(face[1])[2])
            mass += face_mass
            inertia += face_mass * (face[0].magnitude() + face[1].magnitude() + face[0].dot(face[1])) / 6
    print(mass, inertia)
    return mass, inertia


# Entities are for anything that exist within the World.
class Entity:
    def __init__(self, id, **kwargs):
        self.id = id
        self.name = kwargs.get("name", "")

        self.density = kwargs.get("density", 1)
        self.friction = kwargs.get("friction", 0.01)
        self.restitution = kwargs.get("restitution", 0.01)

        self.texture = kwargs.get("texture", None)
        self.texture_loc = kwargs.get("texture_loc", Vector(0, 0))
        self.texture_rot = kwargs.get("texture_rot", 0)

        self.shape = kwargs.get("shape", circle(10))
        self.color = kwargs.get("color", (255, 255, 255))

        self.loc = kwargs.get("loc", Vector(0, 0))
        self.vel = kwargs.get("vel", Vector(0, 0))
        self.rot = kwargs.get("rot", 0)
        self.rot_vel = kwargs.get("rot_vel", 0)

        self.layer = kwargs.get("layer", 1)

        self.vertices = []
        self.aabb = []
        self.update_hitbox()
        self.radius = None if len(self.vertices) > 1 else self.vertices[0].z
        self.mass, self.inertia = find_mass_inertia(self)
        self.mass_inv = 0 if self.mass == 0.0 else 1 / self.mass
        self.inertia_inv = 0 if self.inertia == 0.0 else 1 / self.inertia
        self.affected_by_gravity = kwargs.get("affected_by_gravity", True if self.density > 0 else False)
        self.affected_by_torque = kwargs.get("affected_by_torque", True if self.density > 0 else False)
        self.affected_by_forces = True if self.density > 0 else False

        self.force = Vector(0, 0)
        self.collisions = []
        self.torque = 0

    def update_hitbox(self):
        delta = Matrix3(self.rot)
        self.vertices = [self.loc + delta.dot(point) for point in self.shape]
        if len(self.vertices) > 1:
            x = sorted([vertex.dot((1, 0, 0)) for vertex in self.vertices])
            y = sorted([vertex.dot((0, 1, 0)) for vertex in self.vertices])
            self.aabb = [x[0], x[-1], y[0], y[-1]]
        else:
            radius = self.vertices[0].z
            self.aabb = [self.loc.x - radius, self.loc.x + radius, self.loc.y - radius, self.loc.y + radius]

    def update_physics(self, world):
        if self.density > 0.0:
            self.vel += world.gravity + (self.force * self.mass_inv)
            self.rot_vel += self.torque * self.inertia_inv
        self.loc += self.vel * world.tick_time
        self.rot += self.rot_vel * world.tick_time
        self.update_hitbox()

        self.collisions = []
        self.force = Vector(0.0, 0.0)
        self.torque = 0.0

    def tick(self, world):
        self.update_physics(world)

    def on_collide(self, collision):
        self.collisions.append(collision)
