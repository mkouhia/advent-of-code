"""https://adventofcode.com/2023/day/24"""

import itertools
import re

import numpy as np

from ..base import Puzzle


class Vector:
    def __init__(self, x: int, y: int, z: int, dx: int, dy: int, dz: int):
        self.pos = np.array([x, y, z])
        self.vel = np.array([dx, dy, dz])

    @classmethod
    def from_string(cls, string: str):
        return cls(*list(map(int, re.split("[,@]", string))))

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

    def part1(self) -> str | int:
        """How many particles collide within the test area?"""
        return self.num_intersections((200000000000000, 400000000000000))

    def part2(self) -> str | int:
        return super().part2()
