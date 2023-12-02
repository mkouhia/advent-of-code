"""https://adventofcode.com/2023/day/2"""

import re
from dataclasses import dataclass

from ..base import Puzzle


class CubeConundrum(Puzzle):

    """Analyze game statistics, return possible games."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.games = [Game.from_record(row) for row in input_text.splitlines()]

    def part1(self) -> str:
        """Returns the sum of IDs for games that were possible."""
        return sum(
            g.id_ for g in self.games if g.is_possible(red=12, green=13, blue=14)
        )

    def part2(self) -> str:
        """Returns the sum of power of cube sets."""
        return sum(g.minimum_cubes().power() for g in self.games)


@dataclass
class CubeCombination:
    """Combination of cubes."""

    blue: int = 0
    red: int = 0
    green: int = 0

    @classmethod
    def from_string(cls, spec: str):
        """Create cube combination from string record."""
        parts = spec.strip().split(",")
        detected_cubes = {}
        for part in parts:
            count, col = part.strip().split(" ")
            detected_cubes[col] = int(count)
        return cls(**detected_cubes)

    def power(self) -> int:
        """Return number of cubes multiplied together."""
        return self.red * self.blue * self.green


class Game:

    """Record of a cube game."""

    def __init__(self, id_: int, reveals: list[CubeCombination] = None) -> None:
        self.id_ = id_
        self.reveals = reveals or []

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Game):
            return False

        return __value.id_ == self.id_ and __value.reveals == self.reveals

    def is_possible(self, blue: int, green: int, red: int) -> bool:
        """Is game possible, given maximum number of cubes in the game."""
        for reveal in self.reveals:
            if reveal.blue > blue or reveal.green > green or reveal.red > red:
                return False
        return True

    def minimum_cubes(self) -> CubeCombination:
        """Returns minimum number of cubes that creates possible game."""
        min_cubes = {"blue": 0, "red": 0, "green": 0}
        for reveal in self.reveals:
            for color, prev_amount in min_cubes.items():
                color_amount = getattr(reveal, color)
                if color_amount > prev_amount:
                    min_cubes[color] = color_amount
        return CubeCombination(**min_cubes)

    @classmethod
    def from_record(cls, record: str):
        """Create game from game record in string format."""
        game_str, record_list = record.split(":")
        id_match = re.search(r"Game (\d+)", game_str)
        id_ = int(id_match.group(1))
        records = [CubeCombination.from_string(i) for i in record_list.split(";")]

        return cls(id_, records)
