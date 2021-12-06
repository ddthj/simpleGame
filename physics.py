from Entity import Entity
from LinAlg import cross, Vector
from Suntherland import suntherland


class Collision:
    def __init__(self, a: Entity, b: Entity, axis, gap):
        self.a = a
        self.b = b
        self.axis = axis
        self.gap = gap

        self.relative = Vector(0, 0)

        self.total_impulse = None
        self.normal = Vector(0, 0)
        self.tangent = Vector(0, 0)
        self.manifold = suntherland(self.a.vertices, self.b.vertices)
        if len(self.manifold) > 0:
            self.contact_point = sum(self.manifold) / len(self.manifold)

    def resolve(self):
        a = self.a
        b = self.b
        p = self.contact_point

        # Translate objects apart
        inv_total = a.mass_inv + b.mass_inv
        a.loc += (-self.axis * (self.gap * a.mass * inv_total))
        b.loc += (self.axis * (self.gap * b.mass * inv_total))

        relative_v = a.vel - b.vel + cross(a.rot_vel * (p - a.loc) - b.rot_vel * (p - b.loc))

        e = (a.restitution + b.restitution) / 2
        j = ((-(1 + e) * relative_v).dot(self.axis)) / (self.axis.dot(self.axis * inv_total) )#+ ((cross(p - a.loc).dot(self.axis))**2 / a.inertia) + ((cross(p - b.loc).dot(self.axis))**2 * b.inertia))

        jn = j * self.axis
        a.force += jn
        b.force += -jn
        a.torque += cross(p - a.loc).dot(-jn) * a.inertia_inv
        b.torque += cross(p - b.loc).dot(jn) * b.inertia_inv
        print(a.vel)

        a.on_collide(self)
        b.on_collide(self)
        self.total_impulse = jn.copy()


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
    axes = get_axes(a.vertices) + get_axes(b.vertices)
    min_axis = axes[0]
    min_over = 9999
    for axis in axes:
        ap = sorted([axis.dot(point) for point in a.vertices])
        bp = sorted([axis.dot(point) for point in b.vertices])
        if ap[0] >= bp[-1] or bp[0] >= ap[-1]:
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
