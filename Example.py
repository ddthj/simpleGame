import pygame
from LinAlg import Vector3
from PhysicsObjects import Entity
from World import World
import random
from Suntherland import rectangle

pygame.init()
window = pygame.display.set_mode((1600, 1600))
pygame.display.set_caption("Boats")

square = rectangle(15, 15)
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


ground = Entity("ground",
                points=rect,
                location=Vector3(490, 700, 0),
                mass=0,
                rotation=0.2,
                rvel=0)

wall = Entity("ground",
              points=rect,
              rotation=1.56,
              location=Vector3(-20, 500, 0),
              mass=0)

wall2 = Entity("ground",
               points=rect,
               rotation=1.56,
               location=Vector3(990, 500, 0),
               mass=0)

z = World([ground, wall, wall2])
running = True
clock = pygame.time.Clock()
tick = 0

while running:
    tick += 1

    if len(z.objects) < 55 and tick % 2 == 0 and tick > 120:
        z.objects.append(
            Entity("box",
                   points=square,
                   location=Vector3(500, 200, 0),
                   mass=5,
                   rvel=2,
                   color=good_color())
        )
    window.fill((25, 25, 25))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    z.render(window)
    z.tick()
    pygame.display.update()

    clock.tick(60)
