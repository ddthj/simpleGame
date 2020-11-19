import pygame
from LinAlg import Vector3
from PhysicsObjects import Entity, Material
from World import World
import random
from Suntherland import rectangle, boat

pygame.init()
window = pygame.display.set_mode((1600, 1600))
pygame.display.set_caption("Example")

square = boat(15, 15, 22)  # rectangle(15, 15)
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
                location=Vector3(490, 700, 0),
                material=Material(density=0),
                rotation=0.5,
                rvel=0)

wall = Entity(name="ground1",
              shape=rect,
              rotation=1.56,
              location=Vector3(-20, 500, 0),
              material=Material(density=0))

wall2 = Entity(name="ground2",
               shape=rect,
               rotation=1.56,
               location=Vector3(990, 500, 0),
               material=Material(density=0))


z = World([ground, wall, wall2])
running = True
clock = pygame.time.Clock()
tick = 0

while running:

    if len(z.objects) < 10:
        z.objects.append(
            Entity(
                name="hi",
                shape=boat(15, 15, 35),
                location=Vector3(500, 300, 0),
                rvel=1.0
            )
        )
    tick += 1
    window.fill((25, 25, 25))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    z.render(window)
    z.tick()

    pygame.display.update()

    clock.tick(60)
