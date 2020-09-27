from PhysicsObjects import Entity
from Suntherland import suntherland
import math


class Collision:
    def __init__(self, a: Entity, b: Entity, axis, gap):
        self.a = a
        self.b = b
        self.axis = axis
        self.gap = gap
        self.manifold = None

    def resolve(self):
        # Determine Contact Point
        self.manifold = suntherland(self.a.points, self.b.points)
        contact_point = sum(self.manifold) / len(self.manifold)

        # Translate objects apart
        total = self.a.mass + self.b.mass
        inv_total = self.a.inv_mass + self.b.inv_mass
        if total > 0:
            # Translate objects apart
            self.a.location -= (self.axis * (self.gap * self.a.mass / total))
            self.b.location += (self.axis * (self.gap * self.b.mass / total))

            # Determine direction/distance to contact point and relative velocity at the contact point
            a_to_contact, a_dist = (contact_point - self.a.location).normalize(True)
            b_to_contact, b_dist = (contact_point - self.b.location).normalize(True)
            a_perp = a_to_contact.cross((0, 0, 1))
            b_perp = b_to_contact.cross((0, 0, 1))
            a_point_vel = self.a.velocity + (a_perp * a_dist * self.a.rvel)
            b_point_vel = self.b.velocity + (b_perp * b_dist * self.b.rvel)
            relative_velocity = b_point_vel - a_point_vel

            # Calculate normal and tangent components of velocity
            normal = self.axis
            tangent = self.axis.cross((0, 0, -1))
            normal_velocity = relative_velocity.dot(normal)
            tangent_velocity = relative_velocity.dot(tangent)

            friction = math.sqrt(self.a.friction ** 2 + self.b.friction ** 2)
            restitution = min(self.a.restitution, self.b.restitution) + 1
            normal_impulse = -(restitution * normal_velocity) / inv_total
            tangent_impulse = -(friction * tangent_velocity) / inv_total

            total_impulse = (normal * normal_impulse) + (tangent * tangent_impulse)

            self.a.apply_force(-total_impulse)
            self.b.apply_force(total_impulse)
            self.a.apply_torque(-a_perp.dot(total_impulse))
            self.b.apply_torque(b_perp.dot(total_impulse))


def get_axes(points):
    axes = []
    for i in range(len(points)):
        if i < len(points) - 1:
            axes.append((points[i + 1] - points[i]).normalize().cross((0, 0, 1)))
        else:
            axes.append((points[0] - points[i]).normalize().cross((0, 0, 1)))
    return axes


def sat(collision: Collision):
    a = collision.a
    b = collision.b
    # Returns True if two PhysicsObjects are colliding, as well as the min axis and overlap amount
    axes = get_axes(a.get_points()) + get_axes(b.get_points())
    min_axis = axes[0]
    min_over = 9999
    for axis in axes:
        ap = sorted([axis.dot(point) for point in a.points])
        bp = sorted([axis.dot(point) for point in b.points])
        if ap[0] > bp[-1] or bp[0] > ap[-1]:
            return False
        else:
            a_over = ap[-1] - bp[0]
            b_over = bp[-1] - ap[0]
            if a_over < min_over:
                min_over = a_over
                min_axis = axis
            if b_over < min_over:
                min_over = b_over
                min_axis = -axis  # negative to ensure the axis always points from a to b
    collision.axis = min_axis
    collision.gap = min_over
    return True


def center_rect_collision(a, b):
    if abs(a[0] - b[0]) > a[2] + b[2]:
        return False
    elif abs(a[1] - b[1]) > a[3] + b[3]:
        return False
    return True
