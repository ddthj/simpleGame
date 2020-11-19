import pygame
from LinAlg import Vector3, Matrix3


class Material:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "default")
        self.density = kwargs.get("density", 0.5)
        self.friction = kwargs.get("friction", 0.1)
        self.restitution = kwargs.get("restitution", 0.1)


class HitBox:
    def __init__(self, **kwargs):
        self.shape = kwargs.get("shape", [])
        self.radius = kwargs.get("radius", 0)
        self.color = kwargs.get("color", (255, 255, 255))
        self.type = 1 if self.radius > 0 else 0

        self.vertices = None
        self.center_rectangle = None

    def tick(self, e):
        if self.type:
            self.vertices = [e.location.copy()]
            self.center_rectangle = e.location.x, e.location.y, self.radius, self.radius
        else:
            delta = Matrix3(e.rotation)
            self.vertices = [e.location + delta.dot(point) for point in self.shape]
            x_axis = Vector3(1, 0, 0)
            y_axis = Vector3(0, 1, 0)
            x = sorted([x_axis.dot(vertex) for vertex in self.vertices])
            y = sorted([y_axis.dot(vertex) for vertex in self.vertices])
            min_x = x[0]
            max_x = x[-1]
            min_y = y[0]
            max_y = y[-1]
            x_size = (max_x - min_x) / 2
            y_size = (max_y - min_y) / 2
            self.center_rectangle = min_x + x_size, min_y + y_size, x_size, y_size

    def determine_mass_inertia(self, density):
        mass = 0
        inertia = 0
        if self.type:
            mass = 3.14 * self.radius * self.radius * density
            inertia = 1.57 * self.radius * self.radius * self.radius * self.radius
        else:
            for i in range(len(self.shape)):
                face = (self.shape[i-1], self.shape[i])
                face_mass = density + 0.5 * abs(face[0].cross(face[1])[2])
                mass += face_mass
                inertia += (face_mass * (face[0].magnitude() + face[1].magnitude() + face[0].dot(face[1]))) / 6
        return mass, inertia

    def render(self, window):
        if self.type:
            pygame.draw.circle(window, self.color, self.vertices[0].render(), self.radius, 1)
        else:
            for i in range(len(self.vertices)):
                if i < len(self.vertices) - 1:
                    pygame.draw.line(window, self.color, self.vertices[i].render(), self.vertices[i + 1].render(), 2)
                else:
                    pygame.draw.line(window, self.color, self.vertices[i].render(), self.vertices[0].render(), 2)


class Entity:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.location = kwargs.get("location", Vector3(0, 0, 0))
        self.velocity = kwargs.get("velocity", Vector3(0, 0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.rvel = kwargs.get("rvel", 0)

        self.layer = kwargs.get("layer", 1)

        self.material = kwargs.get("material", Material())

        shape = kwargs.get("shape", None)
        self.hitbox = kwargs.get("hitbox", None)
        if self.hitbox is None and shape is not None:
            self.hitbox = HitBox(shape=shape)
        self.hitbox.tick(self)

        if self.material.density > 0:
            self.mass, self.inertia = self.hitbox.determine_mass_inertia(self.material.density)
            self.inv_mass = 1 / self.mass
        else:
            self.mass = self.inv_mass = self.inertia = 0

        self.affected_by_gravity = True
        self.affected_by_forces = True if self.mass > 0 else False
        self.collidable = True if self.layer > 0 else False
        self.force = Vector3(0, 0, 0)
        self.torque = 0

    def tick(self, time, world):
        self.on_tick(world)
        if self.affected_by_gravity:
            self.apply_force(world.gravity * self.mass)
        if self.affected_by_forces:
            self.velocity += self.force / self.mass
            self.rvel += self.torque / self.inertia
        self.location += self.velocity * time
        self.rotation += self.rvel * time
        self.hitbox.tick(self)
        self.force = Vector3(0, 0, 0)
        self.torque = 0

    def get_vertices(self):
        return self.hitbox.vertices

    def get_center_rectangle(self):
        return self.hitbox.center_rectangle

    def apply_force(self, impulse):
        self.force += impulse

    def apply_torque(self, torque):
        self.torque += torque

    def on_collide(self, collision):
        pass

    def on_tick(self, world):
        pass

    def render(self, window):
        self.hitbox.render(window)
