from Entity import Entity
from Suntherland import suntherland


class Collision:
    def __init__(self, a: Entity, b: Entity, axis, gap):
        self.a = a
        self.b = b
        self.axis = axis
        self.gap = gap

        self.total_impulse = None
        self.manifold = None
        self.contact_point = None

    def resolve(self):
        # Determine Contact Point
        self.manifold = suntherland(self.a.vertices, self.b.vertices)
        if len(self.manifold) > 0:
            self.contact_point = sum(self.manifold) / len(self.manifold)

            # Translate objects apart
            total = 1 / (self.a.mass + self.b.mass)
            # Translate objects apart
            self.a.loc -= (self.axis * (self.gap * self.a.mass * total))
            self.b.loc += (self.axis * (self.gap * self.b.mass * total))

            # Determine direction/distance to contact point and relative velocity at the contact point
            a_to_contact, a_dist = (self.contact_point - self.a.loc).normalize(True)
            b_to_contact, b_dist = (self.contact_point - self.b.loc).normalize(True)
            a_perp = a_to_contact.cross((0, 0, 1))
            b_perp = b_to_contact.cross((0, 0, 1))
            a_point_vel = self.a.vel + (a_perp * a_dist * self.a.rot_vel)
            b_point_vel = self.b.vel + (b_perp * b_dist * self.b.rot_vel)
            relative_velocity = b_point_vel - a_point_vel

            # Calculate normal and tangent components of velocity
            normal = self.axis
            tangent = self.axis.cross((0, 0, -1))
            normal_velocity = relative_velocity.dot(normal)
            tangent_velocity = relative_velocity.dot(tangent)

            friction = self.a.friction + self.b.friction / 2
            restitution = self.a.restitution + self.b.restitution / 2
            normal_impulse = -(restitution * normal_velocity) / total
            tangent_impulse = -(friction * tangent_velocity) / total

            total_impulse = (normal * normal_impulse) + (tangent * tangent_impulse)
            self.total_impulse = total_impulse

            self.a.force -= total_impulse
            self.b.force += total_impulse
            self.a.torque -= a_perp.dot(total_impulse)
            self.b.torque += b_perp.dot(total_impulse)
        # todo - call on_collide functions


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
    axes = get_axes(a.vertices) + get_axes(b.vertices)
    min_axis = axes[0]
    min_over = 9999
    for axis in axes:
        ap = sorted([axis.dot(point) for point in a.vertices])
        bp = sorted([axis.dot(point) for point in b.vertices])
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


def aabb_collision(a, b):
    if a[0] > b[1] or a[1] < b[0] or a[2] > b[3] or a[3] < b[2]:
        return False
    return True
