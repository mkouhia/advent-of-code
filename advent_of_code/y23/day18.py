"""https://adventofcode.com/2023/day/18"""

from dataclasses import dataclass
from enum import Enum

from ..base import Puzzle
from ..helpers import area_by_vertices


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

    @property
    def points(self):
        self._points = [(0, 0)]
        for v in self.vertices:
            self._move(v)
        return self._points

    def _move(self, vertex: Vertex):
        dy, dx = vertex.dir.value
        last = self._points[-1]
        self._points.append((last[0] + dy * vertex.len, last[1] + dx * vertex.len))

    def part1(self) -> str | int:
        self.vertices = [
            Vertex.from_string(i) for i in self.input_text.strip().splitlines()
        ]
        return area_by_vertices(self.points, boundary=1)

    def part2(self) -> str | int:
        self.vertices = [
            Vertex.from_string_hex(i) for i in self.input_text.strip().splitlines()
        ]
        return area_by_vertices(self.points, boundary=1)
