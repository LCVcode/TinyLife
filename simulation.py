from enum import Enum
import random as rng
import numpy as np
from numpy.linalg import norm

class Particle:
    def __init__(self, x, y, id=0):
        self._pos = np.array([x, y]).reshape((1, 2))
        self._id = id
        self._buffer = np.zeros((1, 2))

    @property
    def x(self):
        return self._pos[0][0]

    @x.setter
    def x(self, val):
        self._pos[0][0] = val

    @property
    def y(self):
        return self._pos[0][1]

    @x.setter
    def y(self, val):
        self._pos[0][1] = val

    @property
    def pos(self):
        return np.round(self._pos, 4)

    @property
    def id(self):
        return self._id

    def set_buffer(self, vector):
        self._buffer = vector

    def set_pos(self, vector):
        self._pos = vector


class RuleSet:
    def __init__(self, dim):
        self.fill(0, dim)

    def fill(self, value, dim=None):
        dim = dim or self.dim
        self._val = [[value for _ in range(dim)] for _ in range(dim)]

    @property
    def dim(self):
        return len(self._val)

    def randomize(self):
        for row in self._val:
            for j in range(self.dim):
                row[j] = rng.random() * 2 - 1

    def __getitem__(self, i):
        return self._val[i]

    def make_symmetric(self):
        for i in range(self.dim - 1):
            for j in range(i + 1, self.dim):
                new_val = (self._val[i][j] + self._val[j][i]) / 2
                self._val[i][j] = new_val
                self._val[j][i] = new_val


class BoundaryType(Enum):
    FIXED = 0
    TORUS = 1


class Environment:
    def __init__(self, shape, rule=None, boundary=None):
        self._boundary = boundary or BoundaryType.FIXED
        self._shape = shape
        self._particles = set()
        self._rule = rule

    def set_rule(self, rule):
        if not isinstance(rule, RuleSet):
            raise TypeError("Expected RuleSet")
        self._rule = rule

    @property
    def width(self):
        return self._shape[1]

    @property
    def height(self):
        return self._shape[0]

    @property
    def shape(self):
        return (self.width, self.height)

    def __getitem__(self, i):
        return tuple(self._rule._val[i])

    def add_particle(self, pos, id=0):
        self._particles.add(Particle(*pos, id))

    def tick(self, delta=0.001):
        wid, hei = self.width / 2, self.height / 2

        for p1 in self._particles:
            p1.set_buffer(np.zeros((1, 2)))

            for p2 in self._particles - {p1}:
                diff = p2.pos - p1.pos

                if self._boundary == BoundaryType.TORUS:

                    if diff[0][0] > wid:
                        diff[0][0] -= self.width
                    elif diff[0][0] < -wid:
                        diff[0][0] += self.width

                    if diff[0][1] > hei:
                        diff[0][1] -= self.height
                    elif diff[0][1] < -hei:
                        diff[0][1] += self.height

                dist = norm(diff)

                if dist < 2:  # Overlapping Particles
                    diff = diff * -(dist - 2) ** 2
                else:
                    diff = diff * self._rule[p1._id][p2._id] / (dist**2)

                p1._buffer += diff * delta

        # Move Particles
        for particle in self._particles:
            pos = particle.pos + particle._buffer

            # Fixed boundary condition
            if self._boundary == BoundaryType.FIXED:
                pos[0][0] = max(-wid+1, min(wid-1, pos[0][0]))
                pos[0][1] = max(-hei+1, min(hei-1, pos[0][1]))
            elif self._boundary == BoundaryType.TORUS:
                pos[0][0] = ((pos[0][0] + wid) % self.width) - wid
                pos[0][1] = ((pos[0][1] + hei) % self.height) - hei

            particle.set_pos(pos)

