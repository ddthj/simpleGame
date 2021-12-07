import pygame
from Camera import Camera
from LinAlg import Vector
from Entity import Entity
from World import World
import random
from Shapes import center_rectangle as rect, test


# Generates a vibrant color
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


# Init pygame and create the game window
pygame.init()
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Example")

box = Entity(1, shape=test(), loc=Vector(200, 150), color=good_color(), vel=Vector(-50, 0), rot=0.2)
box2 = Entity(2, shape=rect(50, 100), loc=Vector(50, 175), color=good_color(), vel=Vector(50, 0), rot_vel=1.5)

box3 = Entity(3, shape=rect(50, 100), loc=Vector(-50, -100), color=good_color(), vel=Vector(50, 0), rot_vel=-1.5)
box4 = Entity(4, shape=rect(50, 100), loc=Vector(50, -175), color=good_color(), vel=Vector(-50, 0), rot_vel=-1.5)

ground = Entity(5, shape=rect(500, 20), loc=Vector(0, 0), density=0.0)

# Create a world, and a camera to view the world
world = World((-750, -750, 1500, 1500), (200, 200, 200), [box, box2, box3, box4, ground])
world.gravity = Vector(0, -10)
camera = Camera(True)

# Prepare the main loop
clock = pygame.time.Clock()
running = True
while running:
    # Lock the framerate to 60fps for simplicity
    clock.tick(60)

    # Get any user-input events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            unpaused = True

    world.tick()

    # render each entity
    window.fill((25, 25, 25))
    for item in world.entities:
        # by updating the hitbox of each item we get to see the post-collision view. Otherwise some objects may
        # appear to still be intersecting with each other
        item.update_hitbox()
        camera.render(window, item)
        for c in item.collisions:
            unpaused = False
            camera.render_circle(window, c.contact_point, 2)
            camera.render_line(window, c.contact_point, c.contact_point + (c.axis * 100))
            camera.render_line(window, c.contact_point, c.contact_point + c.normal, (0, 255, 0))
            camera.render_line(window, c.contact_point, c.contact_point + c.tangent, (255, 0, 0))
        # camera.render_aabb(window, item.aabb)
    # camera.render_quadtree(window, world.tree)
    pygame.display.update()
