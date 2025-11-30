import math


def vec_add(v1, v2):
    return [a + b for a, b in zip(v1, v2)]


def vec_sub(v1, v2):
    return [a - b for a, b in zip(v1, v2)]


def vec_mul(v, s):
    return [a * s for a in v]


def vec_cross(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def vec_mag(v):
    return math.sqrt(sum(a * a for a in v))


def vec_norm(v):
    m = vec_mag(v)
    if m == 0:
        return [0, 0, 0]
    return [a / m for a in v]


def get_matrix(pos, fwd, up):
    """Returns a 4x4 transformation matrix."""
    right = vec_norm(vec_cross(up, fwd))
    real_up = vec_norm(vec_cross(fwd, right))

    return [
        [right[0], real_up[0], fwd[0], pos[0]],
        [right[1], real_up[1], fwd[1], pos[1]],
        [right[2], real_up[2], fwd[2], pos[2]],
        [0, 0, 0, 1],
    ]


def get_point_on_curve(t):
    """Generates a point on a demo helix curve."""
    # Scale t to angle
    angle = t * 4 * math.pi  # 2 loops

    # Dimensions
    radius = 200
    height = 100

    # Helix base
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = height * t * 2  # Climb up

    # Add some waviness
    z += 30 * math.sin(t * 8 * math.pi)

    return [x, y, z]


def generate_demo_points(steps=2000):
    points = []
    for i in range(steps + 1):
        t = i / steps
        points.append(get_point_on_curve(t))
    return points
