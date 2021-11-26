from LinAlg import Vector3
from PhysicsObjects import Entity
from pygame import transform, draw
from math import pi


DEGREES = 180 / pi


def cap(x, low, high):
    if x < low:
        return low
    elif x > high:
        return high
    return x


class Camera:
    def __init__(self, debug=False):
        self.location = Vector3(0, 0, 0)
        self.target = None
        self.zoom = 1
        self.debug = debug

    def tick(self):
        if self.target is not None:
            self.location += (self.target.location + (self.target.velocity * Vector3(0.9, 0, 0)) - self.location) / 8

    def render(self, window, entity: Entity):
        offset = Vector3(*window.get_size(), 0) * Vector3(0.5, -0.5, 0)
        if entity.texture is not None:
            rotation = entity.rotation + entity.texture.rotation_offset
            transformed = transform.rotozoom(entity.texture.surface, rotation * DEGREES, self.zoom)
            half = Vector3(*transformed.get_size(), 0) / 2
            loc = (entity.location + entity.texture.location_offset - self.location) * self.zoom - half + offset
            window.blit(transformed, loc.render())
        elif entity.hitbox is not None and self.debug:
            for i in range(len(entity.hitbox.vertices)):
                start = (entity.hitbox.vertices[i - 1] - self.location) * self.zoom + offset
                end = (entity.hitbox.vertices[i] - self.location) * self.zoom + offset
                draw.line(window, entity.hitbox.color, start.render(), end.render(), 2)
