"""https://adventofcode.com/2023/day/18"""

from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from ..base import Puzzle


class Direction(Enum):
    L = (0, -1)
    R = (0, 1)
    D = (-1, 0)
    U = (1, 0)


@dataclass
class Vertex:
    dir: Direction
    len: int
    col: str

    @classmethod
    def from_string(cls, string: str) -> "Vertex":
        parts = string.split(" ")
        return cls(Direction[parts[0]], int(parts[1]), parts[2][1:-1])

    @classmethod
    def from_string_hex(cls, string: str) -> "Vertex":
        parts = string.split(" ")
        hex_ = parts[2][1:-1]
        dist_val = int(hex_[1:-1], 16)
        dir_s = {"0": "R", "1": "D", "2": "L", "3": "U"}
        dir = Direction[dir_s[hex_[-1]]]
        return cls(dir, dist_val, hex_)


class LavaductLagoon(Puzzle):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self._points = []
        self.vertices = []

    @cached_property
    def points(self):
        self._points = [(0, 0)]
        for v in self.vertices:
            self._move(v)
        return self._points

    def _move(self, vertex: Vertex):
        dy, dx = vertex.dir.value
        last = self._points[-1]
        self._points.append((last[0] + dy * vertex.len, last[1] + dx * vertex.len))

    def area(self, boundary=1):
        """Returns area bound by vertices.

        Employs Shoelace formula.
        """
        a = 0
        ab = 0
        y0, x0 = self.points[0]
        for [y1, x1] in self.points[1:]:
            dx = x1 - x0
            dy = y1 - y0
            a += 0.5 * (y0 * dx - x0 * dy)
            if boundary:
                ab += abs(dy) + abs(dx)
            x0 = x1
            y0 = y1
        return int(a + (ab / 2 + 1 if boundary else 0))

    def part1(self) -> str | int:
        self.vertices = [
            Vertex.from_string(i) for i in self.input_text.strip().splitlines()
        ]
        return self.area()

    def part2(self) -> str | int:
        self.vertices = [
            Vertex.from_string_hex(i) for i in self.input_text.strip().splitlines()
        ]
        return self.area()
