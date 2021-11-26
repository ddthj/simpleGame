from math import pi
import pygame
from Camera import Camera
from LinAlg import Vector3
from PhysicsObjects import Entity, Material
from World import World
import random
from Suntherland import center_rectangle as rectangle, boat

pygame.init()
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Example")

square = boat(15, 15, 22)
rect = rectangle(500, 50)


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


ground = Entity(name="ground0",
                shape=rect,
                location=Vector3(0, 0, 0),
                material=Material(density=0, restitution=0.9),
                rotation=1.0,
                rvel=-0.1)

wall = Entity(name="ground1",
              shape=rect,
              rotation=pi/2,
              location=Vector3(-250, 0, 0),
              material=Material(density=0))

wall2 = Entity(name="ground2",
               shape=rect,
               rotation=pi/2,
               location=Vector3(250, 0, 0),
               material=Material(density=0))


y = Camera(True)
z = World((-2000, -2000, 4000, 4000), (200, 200, 200), [ground, wall, wall2])
running = True
clock = pygame.time.Clock()
tick = 0

while running:

    if len(z.objects) < 10 and tick > 200:
        z.objects.append(
            Entity(
                name="hi",
                shape=boat(15, 15, 35),
                location=Vector3(0, 300, 0),
                rvel=1.0,
                color=good_color(),
                material=Material(restitution=0.9)
            )
        )
    tick += 1
    window.fill((25, 25, 25))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    z.tick()
    for item in z.objects:
        y.render(window, item)
    pygame.display.update()

    clock.tick(60)
