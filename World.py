from Physics import *
from LinAlg import Vector3
from pygame import draw


class QuadTree:
    def __init__(self, depth, rect):
        self.max_depth = 3
        self.max_objects = 8
        self.depth = depth
        self.rect = rect
        self.center_rect = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2, rect[2] / 2, rect[3] / 2)
        self.objects = []
        self.nodes = []

    def clear(self):
        self.objects = []
        self.nodes = []

    def split(self):
        width = self.rect[2] / 2
        height = self.rect[3] / 2
        self.nodes.append(QuadTree(self.depth + 1, (self.rect[0], self.rect[1], width, height)))
        self.nodes.append(QuadTree(self.depth + 1, (self.rect[0] + width, self.rect[1], width, height)))
        self.nodes.append(QuadTree(self.depth + 1, (self.rect[0], self.rect[1] + height, width, height)))
        self.nodes.append(QuadTree(self.depth + 1, (self.rect[0] + width, self.rect[1] + height, width, height)))
        for obj in self.objects:
            self.insert(obj)
        self.objects = []

    def touching(self, rect):
        return center_rect_collision(self.center_rect, rect)

    def insert(self, obj):
        child = True
        for node in self.nodes:
            child = False
            node.insert(obj)
        if child and self.touching(obj.get_center_rect()):
            self.objects.append(obj)
            if len(self.objects) > self.max_objects and self.depth < self.max_depth:
                self.split()

    def get_child_nodes(self):
        child = True
        temp = []
        for node in self.nodes:
            child = False
            temp += node.get_child_nodes()
        if child:
            return [self.objects]
        return temp

    def render(self, window):
        origin = Vector3(self.rect[0], self.rect[1], 0)
        left = origin + Vector3(self.rect[2], 0, 0)
        up = origin + Vector3(0, self.rect[3], 0)
        opposite = origin + Vector3(self.rect[2], self.rect[3], 0)
        draw.line(window, (200, 100, 200), origin.render(), left.render(), 2)
        draw.line(window, (200, 100, 200), origin.render(), up.render(), 2)
        draw.line(window, (200, 100, 200), left.render(), opposite.render(), 2)
        draw.line(window, (200, 100, 200), up.render(), opposite.render(), 2)
        for node in self.nodes:
            node.render(window)


class World:
    def __init__(self, objects):
        self.gravity = Vector3(0, 10, 0)
        self.tick_time = 0.0333333333333334
        self.tree = QuadTree(0, (0, 0, 1000, 1000))
        self.objects = objects

    def tick(self):
        self.tree.clear()
        for obj in self.objects:
            obj.tick(self.tick_time, self)
            if obj.collidable:
                self.tree.insert(obj)

        potential_collisions = []
        cull_tracker = {x: [] for x in self.objects}
        for node in self.tree.get_child_nodes():
            for a in node:
                for b in node:
                    if a != b and a.layer & b.layer and b not in cull_tracker[a]:
                        if center_rect_collision(a.get_center_rect(), b.get_center_rect()):
                            potential_collisions.append(Collision(a, b, None, None))
                            cull_tracker[a].append(b)
                            cull_tracker[b].append(a)

        for collision in potential_collisions:
            if sat(collision):
                collision.resolve()

    def render(self, window):
        self.tree.render(window)
        for item in self.objects:
            item.render(window)
