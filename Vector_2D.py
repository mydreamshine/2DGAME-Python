import math


class Vector_2D:
    def __init__(self, x = 0.0, y = 0.0):
        self.x, self.y = (x, y)

    def __add__(self, other): # A + B
        return Vector_2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other): # A += B
        self.x += other.x
        self.y += other.y

    def __sub__(self, other): # A - B
        return Vector_2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other): # A -= B
        self.x -= other.x
        self.y -= other.y

    def __neg__(self): # -A
        return Vector_2D(-self.x, -self.y)

    def __mul__(self, scalar): # A * scalar
        return Vector_2D(self.x * scalar, self.y * scalar)

    def __imul__(self, other): # A *= B
        self.x *= other.x
        self.y *= other.y

    def __truediv__(self, scalar): # A / scalar
        return Vector_2D(self.x / scalar, self.y / scalar)

    def __itruediv__(self, scalar): # A /= scalar
        self.x /= scalar
        self.y /= scalar

    def dot(self, other):
        return self.x * other.x + self.y + other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def magnitude(self): # 벡터 크기
        return math.sqrt(self.dot(self))


def unit(Vector):
    return Vector / Vector.magnitude()


def normalize(Vector):
    Vector /= Vector.magnitude()