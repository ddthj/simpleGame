from LinAlg import Vector
from Entity import Entity
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
        self.location = Vector(0, 0, 0)
        self.target = None
        self.zoom = 1
        self.debug = debug

    def tick(self):
        if self.target is not None:
            self.location += (self.target.location + (self.target.velocity * Vector(0.9, 0, 0)) - self.location) / 8

    def render(self, window, entity: Entity):
        offset = Vector(*window.get_size(), 0) * Vector(0.5, -0.5, 0)
        if entity.texture is not None:
            rotation = entity.rot + entity.texture_rot
            transformed = transform.rotozoom(entity.texture, rotation * DEGREES, self.zoom)
            half = Vector(*transformed.get_size(), 0) / 2
            loc = (entity.loc + entity.texture_loc - self.location) * self.zoom - half + offset
            window.blit(transformed, loc.render())
        elif self.debug:
            for i in range(len(entity.vertices)):
                start = (entity.vertices[i - 1] - self.location) * self.zoom + offset
                end = (entity.vertices[i] - self.location) * self.zoom + offset
                draw.line(window, entity.color, start.render(), end.render(), 2)

    def render_aabb(self, window, a):
        offset = Vector(*window.get_size(), 0) * Vector(0.5, -0.5, 0)
        vertices = [Vector(a[0], a[2], 0),
                    Vector(a[1], a[2], 0),
                    Vector(a[1], a[3], 0),
                    Vector(a[0], a[3], 0)]
        for i in range(4):
            start = (vertices[i - 1] - self.location) * self.zoom + offset
            end = (vertices[i] - self.location) * self.zoom + offset
            draw.line(window, [255, 200, 255], start.render(), end.render(), 2)

    def render_quadtree(self, window, tree):
        self.render_aabb(window, tree.aabb)
        for node in tree.nodes:
            self.render_quadtree(window, node)
