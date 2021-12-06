import pygame
from Camera import Camera
from LinAlg import Vector
from Entity import Entity
from Physics import Collision, sat
from Shapes import center_rectangle
from Suntherland import suntherland

pygame.init()
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
camera = Camera(True)

color = (0, 255, 255)

a = Entity(1, shape=center_rectangle(100, 100), loc=Vector(-50, -50), color=color)
b = Entity(2, shape=center_rectangle(100, 100), loc=Vector(50, 50), color=color, density=1)
follow = False
running = True
while running:
    window.fill((25, 25, 25))
    events = pygame.event.get()
    mouse_pos = Vector(*pygame.mouse.get_pos())
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            follow = True
        elif event.type == pygame.MOUSEBUTTONUP:
            follow = False
    if follow:
        a.loc = camera.mouse_to_world(window, mouse_pos)
        a.update_hitbox()

    x = None
    c = Collision(a, b, None, None)

    if sat(c):
        manifold = suntherland(a.vertices, b.vertices)
        x = Entity(3, shape=manifold, color=(255, 0, 0))

    camera.render(window, a)
    camera.render(window, b)

    if x is not None:
        if True:  # not follow:
            c.resolve()
            a.update_hitbox()
            b.update_hitbox()
        camera.render(window, x)
        camera.render_circle(window, c.contact_point, 2)
        camera.render_line(window, c.contact_point, c.contact_point + (c.axis * 100))

    pygame.display.update()
