from LinAlg import Vector


def circle(x):
    return [Vector(0, 0, x)]


def center_rectangle(x, y):
    x /= 2
    y /= 2
    return [Vector(x, y, 0), Vector(x, -y, 0), Vector(-x, -y, 0), Vector(-x, y, 0)]


def corner_rectangle(x, y):
    return [Vector(0, 0, 0), Vector(x, 0, 0), Vector(x, y, 0), Vector(0, y, 0)]


def ramp(x, y):
    return [Vector(0, 0, 0), Vector(x, 0, 0), Vector(0, y, 0)]


def boat(x, y, z):
    return [Vector(0, z, 0), Vector(x, y, 0), Vector(x, -y, 0), Vector(-x, -y, 0), Vector(-x, y, 0)]
