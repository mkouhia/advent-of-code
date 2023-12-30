"""https://adventofcode.com/2023/day/24"""

import itertools
import re

import numpy as np
import sympy

from ..base import Puzzle


class Vector:
    def __init__(self, x: int, y: int, z: int, dx: int, dy: int, dz: int):
        self.pos = np.array([x, y, z])
        self.vel = np.array([dx, dy, dz])

    @classmethod
    def from_string(cls, string: str):
        return cls(*list(map(int, re.split("[,@]", string))))

    def tolist(self):
        return self.pos.tolist() + self.vel.tolist()

    @property
    def k2d(self):
        return self.vel[1] / self.vel[0]

    def __repr__(self):
        return "<Hailstone({}, {}, {} @ {}, {}, {})>".format(*self.pos, *self.vel)

    def paths_intersect_xy(self, other: "Vector"):
        """Calculate point, where paths intersect on xy plane.

        Returns:
            Point, where paths intersect. If there is no intersection,
            returns None.
        """
        # Check parallel paths
        if abs(self.k2d) == abs(other.k2d):
            # Check if other's origin is on self's line
            ty = (other.pos[1] - self.pos[1]) / self.vel[1]
            tx = (other.pos[0] - self.pos[0]) / self.vel[0]
            if ty == tx:
                return 1
            return 0

        a = np.hstack((self.vel[:2].reshape(-1, 1), (-other.vel[:2]).reshape(-1, 1)))
        b = other.pos[:2] - self.pos[:2]
        t_xy = np.linalg.solve(a, b)

        if np.any(t_xy < 0):
            # Hailstones' paths crossed in the past
            return -1

        new_0 = self.pos + t_xy[0] * self.vel

        return new_0[:2]


class NeverTellMeTheOdds(Puzzle):

    """Never tell me the odds.

    Particle trajectory matching.
    """

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.particles = [
            Vector.from_string(s) for s in input_text.strip().splitlines()
        ]

    def num_intersections(self, limits):
        count = 0
        for p1, p2 in itertools.combinations(self.particles, 2):
            pos = p1.paths_intersect_xy(p2)
            if isinstance(pos, int):
                if pos == 1:
                    count += 1
                continue

            x, y = pos
            if limits[0] <= x <= limits[1] and limits[0] <= y <= limits[1]:
                count += 1

        return count

    def find_intersecting_path(self) -> Vector:
        """Find path, which intersects with all hailstones.

        The path is found by first three stones, with equations
            p + v * ti = pi + vi * ti ,
        thus
            x + vx * ti = xi + vxi * ti
            y + vy * ti = yi + vyi * ti
            z + vz * ti = zi + vzi * ti

        and then equating ti out from each pair of equations.

        Returns:
            Intersecting vector with integer components.
        """
        x, y, z, vx, vy, vz = sympy.symbols("x0, y0, z0, vx0, vy0, vz0")
        x1, y1, z1, vx1, vy1, vz1 = self.particles[0].tolist()
        x2, y2, z2, vx2, vy2, vz2 = self.particles[1].tolist()
        x3, y3, z3, vx3, vy3, vz3 = self.particles[2].tolist()

        sols = sympy.solve(
            [
                (x1 - x) * (vy - vy1) - (y1 - y) * (vx - vx1),
                (y1 - y) * (vz - vz1) - (z1 - z) * (vy - vy1),
                (x2 - x) * (vy - vy2) - (y2 - y) * (vx - vx2),
                (y2 - y) * (vz - vz2) - (z2 - z) * (vy - vy2),
                (x3 - x) * (vy - vy3) - (y3 - y) * (vx - vx3),
                (y3 - y) * (vz - vz3) - (z3 - z) * (vy - vy3),
            ],
            (x, y, z, vx, vy, vz),
        )
        for sol in sols:
            if all(isinstance(v, sympy.core.numbers.Integer) for v in sol):
                return Vector(*[int(v) for v in sol])

    def part1(self) -> str | int:
        """How many particles collide within the test area?"""
        return self.num_intersections((200000000000000, 400000000000000))

    def part2(self) -> str | int:
        vec = self.find_intersecting_path()
        return int(sum(vec.pos))
