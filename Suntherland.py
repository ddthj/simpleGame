from LinAlg import Vector3
import pygame


def rectangle(x, y):
    return [Vector3(x, y, 0), Vector3(x, -y, 0), Vector3(-x, -y, 0), Vector3(-x, y, 0)]


def render_polygon(poly, color, window, loop=True):
    for i in range(len(poly)):
        if i + 1 < len(poly):
            a = poly[i].copy().render()
            b = poly[i + 1].copy().render()
        elif loop:
            a = poly[i].copy().render()
            b = poly[0].copy().render()
        else:
            break
        pygame.draw.line(window, color, a, b)


# confirms that a polygon is both clockwise-defined and convex
def clockwise_convex(polygon):
    x = len(polygon)
    if x > 0:
        for i in range(x - 1):
            l1 = (polygon[(i + 1) % x] - polygon[i % x]).normalize().cross((0, 0, 1))
            l2 = (polygon[(i + 2) % x] - polygon[(i + 1) % x]).normalize()
            if l1.dot(l2) <= 0:
                return False
        return True
    return False


# Clips a subject polygon within the area of the scissors polygon. The scissors polygon must be convex
def suntherland(subject, scissors):
    def inside(p):
        return (v2[0] - v1[0]) * (p[1] - v1[1]) <= (v2[1] - v1[1]) * (p[0] - v1[0])

    def intersection():
        dc = [v1[0] - v2[0], v1[1] - v2[1]]
        dp = [s[0] - vertex[0], s[1] - vertex[1]]
        n1 = v1[0] * v2[1] - v1[1] * v2[0]
        n2 = s[0] * vertex[1] - s[1] * vertex[0]
        n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
        return Vector3((n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3, 0)

    output = subject
    v1 = scissors[-1]

    for v2 in scissors:
        input_list = output
        output = []
        s = input_list[-1]

        for vertex in input_list:
            if inside(vertex):
                if not inside(s):
                    output.append(intersection())
                output.append(vertex)
            elif inside(s):
                output.append(intersection())
            s = vertex
        v1 = v2
    return output


def suntherland_debug(subject, scissors, window):
    def inside(p):
        return (v2[0] - v1[0]) * (p[1] - v1[1]) < (v2[1] - v1[1]) * (p[0] - v1[0])

    def intersection():
        dc = [v1[0] - v2[0], v1[1] - v2[1]]
        dp = [s1[0] - s2[0], s1[1] - s2[1]]
        n1 = v1[0] * v2[1] - v1[1] * v2[0]
        n2 = s1[0] * s2[1] - s1[1] * s2[0]
        n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
        return Vector3((n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3, 0)

    print(clockwise_convex(subject), clockwise_convex(scissors))
    output = subject
    v1 = scissors[-1]

    for v2 in scissors:
        input_list = output
        output = []
        s1 = input_list[-1]

        for s2 in input_list:
            input(">")
            window.fill((0, 0, 0))
            render_polygon(scissors, (255, 0, 0), window)
            if len(input_list) > 1:
                render_polygon(input_list, (0, 255, 255), window)
            if len(output) > 1:
                render_polygon(output, (0, 255, 0), window, False)
            pygame.draw.line(window, (255, 0, 255), v1.copy().render(), v2.copy().render(), 2)
            pygame.draw.line(window, (255, 255, 0), s1.copy().render(), s2.copy().render(), 2)
            pygame.display.update()
            pygame.event.get()

            if inside(s2):
                print("s2 inside")
                if not inside(s1):
                    print("s1 outside, intersection")
                    output.append(intersection())
                output.append(s2)
            elif inside(s1):
                print("s1 inside, intersection")
                output.append(intersection())
            else:
                print("both outside")
            s1 = s2
        v1 = v2
    return output
