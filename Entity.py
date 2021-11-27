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
            face_mass = entity.density + 0.5 * abs(face[0].cross(face[1])[2])
            mass += face_mass
            inertia += (face_mass * (face[0].magnitude() + face[1].magnitude() + face[0].dot(face[1]))) / 6
    return mass, inertia


# Entities are for anything that exist within the World.
class Entity:
    def __init__(self, id, **kwargs):
        self.id = id
        self.name = kwargs.get("name", "")

        self.density = kwargs.get("density", 0.5)
        self.friction = kwargs.get("friction", 0.1)
        self.restitution = kwargs.get("restitution", 0.1)

        self.texture = kwargs.get("texture", None)
        self.texture_loc = kwargs.get("texture_loc", Vector())
        self.texture_rot = kwargs.get("texture_rot", 0)

        self.shape = kwargs.get("shape", circle(10))
        self.color = kwargs.get("color", (255, 255, 255))

        self.loc = kwargs.get("loc", Vector())
        self.vel = kwargs.get("vel", Vector())
        self.rot = kwargs.get("rot", 0)
        self.rot_vel = kwargs.get("rot_vel", 0)

        self.layer = kwargs.get("layer", 1)

        self.vertices = []
        self.aabb = []
        self.update_hitbox()
        self.radius = None if len(self.vertices) > 1 else self.vertices[0].z
        self.mass, self.inertia = find_mass_inertia(self)
        self.inv_mass = 1 / self.mass if self.mass > 0 else 0
        self.inv_inertia = 1 / self.inertia if self.inertia > 0 else 0

        self.affected_by_gravity = kwargs.get("affected_by_gravity", True if self.density > 0 else False)
        self.affected_by_torque = kwargs.get("affected_by_torque", True if self.density > 0 else False)
        self.affected_by_forces = True if self.density > 0 else False

        self.force = Vector()
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

    def update(self, world):
        if self.affected_by_gravity:
            self.force += world.gravity * self.mass
        self.vel += self.force * self.inv_mass
        self.rot_vel += self.torque * self.inv_inertia
        self.loc += self.vel * world.tick_time
        self.rot += self.rot_vel * world.tick_time
        self.update_hitbox()

        self.on_tick(world)

        self.force = Vector(0, 0, 0)
        self.torque = 0

    def on_tick(self, world):
        pass

    def on_collide(self, collision):
        pass

