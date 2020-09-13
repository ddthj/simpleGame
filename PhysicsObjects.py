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
        self.mass = kwargs.get("mass", 10)
        self.inv_mass = 1 / self.mass if self.mass != 0 else 0
        self.friction = kwargs.get("friction", 0.1)
        self.restitution = kwargs.get("restitution", 0.1)
        self.inertia = kwargs.get("moment", self.mass ** 2.5)

        self.color = kwargs.get("color", (255, 255, 255))

        self.gravity = True
        self.force = Vector3(0, 0, 0)
        self.torque = 0

    def determine_points(self):
        delta = Matrix3(self.rotation)
        return [self.location + delta.dot(point) for point in self.raw_points]

    def determine_center_rect(self):
        x_axis = Vector3(1, 0, 0)
        y_axis = Vector3(0, 1, 0)
        x = [x_axis.dot(point) for point in self.get_points()]
        y = [y_axis.dot(point) for point in self.get_points()]
        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)
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
        if self.gravity:
            self.apply_force(world.gravity)
        if self.mass > 0:
            self.velocity += self.force / self.mass
            self.rvel += self.torque / self.inertia
        self.location += self.velocity * time
        self.rotation += self.rvel * time
        self.points = self.determine_points()
        self.center_rect = self.determine_center_rect()
        self.force = Vector3(0, self.gravity, 0)
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
