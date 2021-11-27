import pygame
from Camera import Camera
from LinAlg import Vector
from Entity import Entity
from World import World
import random
from Shapes import center_rectangle as rect


def good_color():
    while 1:
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        da = abs(a - b)
        db = abs(b - c)
        dc = abs(c - a)
        if int((da + db + dc) / 3) > 150:
            break
    return a, b, c


class GUID:
    def __init__(self):
        self.id = 0

    def get(self):
        self.id += 1
        return self.id


class MagicBox(Entity):
    def on_tick(self, world):
        if self.loc.y < -500:
            self.loc.y = 500
            if len(world.entities) < 100:
                world.entities.append(MagicBox(g.get(), shape=rect(25, 25), loc=Vector(0, 400), color=good_color()))



pygame.init()
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Example")
clock = pygame.time.Clock()

g = GUID()

ground = Entity(g.get(), shape=rect(500, 50), loc=Vector(0, 0), density=0, rot_vel=0.1)
wall1 = Entity(g.get(), shape=rect(50, 500), loc=Vector(-250, 0), density=0)
wall2 = Entity(g.get(), shape=rect(50, 500), loc=Vector(250, 0), density=0)
box = MagicBox(g.get(), shape=rect(25, 25), loc=Vector(0, 400), color=good_color())

camera = Camera(True)
world = World((-750, -750, 1500, 1500), (200, 200, 200), [ground, wall1, wall2, box])

running = True
while running:
    window.fill((25, 25, 25))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    world.tick()
    for item in world.entities:
        camera.render(window, item)
        # camera.render_aabb(window, item.aabb)
    # camera.render_quadtree(window, world.tree)

    pygame.display.update()
    clock.tick(60)
