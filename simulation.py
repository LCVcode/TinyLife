from enum import Enum
import random as rng
import numpy as np
from numpy.linalg import norm

class Particle:
    def __init__(self, x, y, id=0):
        self._pos = np.array([x, y]).reshape((1, 2))
        self._vel = np.array([0, 0]).reshape((1, 2))
        self._id = id

    @property
    def x(self):
        return self._pos[0][0]

    @x.setter
    def x(self, val):
        self._pos[0][0] = val

    @property
    def y(self):
        return self._pos[0][1]

    @y.setter
    def y(self, val):
        self._pos[0][1] = val

    @property
    def vx(self):
        return self._vel[0][0]

    @vx.setter
    def vx(self, val):
        self._vel[0][0] = val

    @property
    def vy(self):
        return self._vel[0][1]

    @vy.setter
    def vy(self, val):
        self._vel[0][1] = val

    @property
    def pos(self):
        return np.round(self._pos, 4)

    @property
    def vel(self):
        return np.round(self._vel, 4)

    @property
    def id(self):
        return self._id

    def set_buffer(self, vector):
        self._buffer = vector

    def set_pos(self, vector):
        self._pos = vector

    def set_vel(self, vector):
        self._vel = vector


class ForceGraph:
    C = 2
    MIN_X1 = 2
    def __init__(self, x1, x2, x3, a, c=None):
        c = c or ForceGraph.C
        x1, x2, x3 = sorted((x1, x2, x3))
        self._data = (x1, x2, x3, a, c)

    def get_at(self, x):
        x = abs(x)

        # Particles too far separated
        if x > self._data[2]:
            return 0

        # Partle repulsion force
        if x < self._data[0]:
            a = -self._data[4] / (self._data[0]**2)
            b = (2 * self._data[4]) / self._data[0]
            c = -self._data[4]
            return a * x**2 + b * x + c

        # First half of attraction zone
        if x < self._data[1]:
            m = self._data[3] / (self._data[1] - self._data[0])
            b = -m * self._data[0]
        # Second half of attraction zone
        else:
            m = -self._data[3] / (self._data[2] - self._data[1])
            b = -m * self._data[2]

        return m * x + b

class RuleSet:
    def __init__(self, dim):
        self._dim = dim
        self._forces = [None for _ in range(dim**2)]

    @property
    def dim(self):
        return self._dim

    def randomize(self):
        for i in range(len(self._forces)):
            x1 = rng.uniform(ForceGraph.MIN_X1, 10)
            x2 = rng.uniform(ForceGraph.MIN_X1, 20)
            x3 = rng.uniform(ForceGraph.MIN_X1, 30)
            self._forces[i] = ForceGraph(x1, x2, x3, 5, 5)

    def __getitem__(self, i):
        return self._forces[i]

    def make_symmetric(self):
        for i in range(self._dim - 1):
            for j in range(i + 1, self._dim):
                self._forces[self._dim * i + j] = self._forces[self._dim * j + i]


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

    def add_random_particle(self):
        pos = (rng.uniform(0, self.width), rng.uniform(0, self.height))
        _id = rng.randint(0, self._rule.dim - 1)
        self.add_particle(pos, _id)

    def tick(self, delta=0.001):
        wid, hei = self.width / 2, self.height / 2

        for p1 in self._particles:
            p1.set_buffer(np.zeros((1, 2)))
            p1._limits = list()

            for p2 in self._particles - {p1}:
                rule = self._rule[self._rule.dim * p1._id + p2._id]
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

                '''
                if dist < 2:  # Overlapping Particles
                    p1._limits.append(diff / dist)
                    diff = diff * -(dist - 2) ** 2
                else:  # Apply rule
                    diff = diff * self._rule[p1._id][p2._id] / (dist**2)
                '''

                diff = rule.get_at(dist) * diff / dist

                p1._buffer += diff * delta

        # Move Particles
        for particle in self._particles:

            # Apply Particle limits, if any
            for lim in particle._limits:
                x = particle._buffer.dot(lim.T)
                if x > 0:
                    particle._buffer -= lim * x

            pos = particle.pos + particle._buffer

            # Fixed boundary condition
            if self._boundary == BoundaryType.FIXED:
                pos[0][0] = max(-wid+1, min(wid-1, pos[0][0]))
                pos[0][1] = max(-hei+1, min(hei-1, pos[0][1]))
            elif self._boundary == BoundaryType.TORUS:
                pos[0][0] = ((pos[0][0] + wid) % self.width) - wid
                pos[0][1] = ((pos[0][1] + hei) % self.height) - hei

            particle.set_pos(pos)


if __name__ == '__main__':
    demo = ForceGraph(2, 4, 6, 10, 5)
    for i in np.arange(0, 11, 0.25):
        print(i, demo.get_at(i))

