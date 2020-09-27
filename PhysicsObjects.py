import pygame
from LinAlg import Vector3, Matrix3


class Entity:
    def __init__(self, name, **kwargs):
        self.name = name
        self.location = kwargs.get("location", Vector3(0, 0, 0))
        self.rotation = kwargs.get("rotation", 0)
        self.velocity = kwargs.get("velocity", Vector3(0, 0, 0))
        self.rvel = kwargs.get("rvel", 0)

        self.raw_points = kwargs.get("points", [])
        self.points = self.determine_points()
        self.center_rect = self.determine_center_rect()

        self.layer = kwargs.get("layer", 1)

        self.density = kwargs.get("density", 0.5)
        if self.density > 0:
            self.mass, self.inertia = self.determine_mass_inertia()
            self.inv_mass = 1 / self.mass
        else:
            self.mass = self.inv_mass = self.inertia = 0

        self.friction = kwargs.get("friction", 0.1)
        self.restitution = kwargs.get("restitution", 0.1)

        self.color = kwargs.get("color", (255, 255, 255))

        self.affected_by_gravity = True
        self.affected_by_forces = True if self.mass > 0 else False
        self.collidable = True if self.layer > 0 else False
        self.force = Vector3(0, 0, 0)
        self.torque = 0

    def determine_faces(self):
        points = self.raw_points
        faces = []
        for i in range(len(points)):
            if i < len(points) - 1:
                faces.append((points[i], points[i+1]))
            else:
                faces.append((points[i], points[0]))
        return faces

    def determine_mass_inertia(self):
        mass = 0
        inertia = 0
        for face in self.determine_faces():
            face_mass = self.density + 0.5 * abs(face[0].cross(face[1])[2])
            mass += face_mass
            inertia = face_mass * (face[0].magnitude() + face[1].magnitude() + face[0].dot(face[1])) / 6
        return mass, inertia

    def determine_points(self):
        delta = Matrix3(self.rotation)
        return [self.location + delta.dot(point) for point in self.raw_points]

    def determine_center_rect(self):
        x_axis = Vector3(1, 0, 0)
        y_axis = Vector3(0, 1, 0)
        x = sorted([x_axis.dot(point) for point in self.get_points()])
        y = sorted([y_axis.dot(point) for point in self.get_points()])
        min_x = x[0]
        max_x = x[-1]
        min_y = y[0]
        max_y = y[-1]
        x_size = (max_x - min_x) / 2
        y_size = (max_y - min_y) / 2
        return min_x + x_size, min_y + y_size, x_size, y_size

    def get_points(self):
        if self.points is None:
            self.points = self.determine_points()
        return self.points

    def get_center_rect(self):
        if self.center_rect is None:
            self.center_rect = self.determine_center_rect()
        return self.center_rect

    def apply_force(self, impulse):
        self.force += impulse

    def apply_torque(self, torque):
        self.torque += torque

    def tick(self, time, world):
        self.on_tick(world)
        if self.affected_by_gravity:
            self.apply_force(world.gravity * self.mass)
        if self.affected_by_forces:
            self.velocity += self.force / self.mass
            self.rvel += self.torque / self.inertia
        self.location += self.velocity * time
        self.rotation += self.rvel * time
        self.points = self.determine_points()
        self.center_rect = self.determine_center_rect()
        self.force = Vector3(0, 0, 0)
        self.torque = 0

    def on_collide(self, collision):
        pass

    def on_tick(self, world):
        pass

    def render(self, window):
        for i in range(len(self.points)):
            if i < len(self.points) - 1:
                pygame.draw.line(window, self.color, self.points[i].render(), self.points[i + 1].render(), 2)
            else:
                pygame.draw.line(window, self.color, self.points[i].render(), self.points[0].render(), 2)
