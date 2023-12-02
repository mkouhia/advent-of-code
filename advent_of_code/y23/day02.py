"""https://adventofcode.com/2023/day/2"""

import re
from dataclasses import dataclass

from ..base import Puzzle


class CubeConundrum(Puzzle):

    """Analyze game statistics, return possible games."""
    
    def part1(self) -> str:
        """Returns the sum of IDs for games that were possible."""
        games = self.parse_games(self.input_text)
        return sum(g.id for g in games if g.is_possible(red=12, green=13, blue=14))

    def part2(self) -> str:
        """Returns the sum of power of cube sets."""
        games = self.parse_games(self.input_text)
        return sum(g.minimum_cubes().power() for g in games)

    @staticmethod
    def parse_games(spec: str):
        return [Game.from_record(row) for row in spec.splitlines()]


@dataclass
class CubeCombination:
    """Combination of cubes."""

    blue: int = 0
    red: int = 0
    green: int = 0

    @classmethod
    def from_string(cls, spec: str):
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
    def __init__(self, id: int, reveals: list[CubeCombination] = None) -> None:
        self.id = id
        self.reveals = reveals or []

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Game):
            return False

        return __value.id == self.id and __value.reveals == self.reveals

    def is_possible(self, blue: int, green: int, red: int) -> bool:
        """Is game possible, given maximum number of cubes in the game."""
        for round in self.reveals:
            if round.blue > blue or round.green > green or round.red > red:
                return False
        return True

    def minimum_cubes(self) -> CubeCombination:
        """Returns minimum number of cubes that creates possible game."""
        min_cubes = {"blue": 0, "red": 0, "green": 0}
        for round in self.reveals:
            for color in min_cubes:
                color_amount = getattr(round, color)
                if color_amount > min_cubes[color]:
                    min_cubes[color] = color_amount
        return CubeCombination(**min_cubes)

    @classmethod
    def from_record(cls, record: str):
        game_str, record_list = record.split(":")
        id_match = re.search(r"Game (\d+)", game_str)
        id = int(id_match.group(1))
        records = [CubeCombination.from_string(i) for i in record_list.split(";")]

        return cls(id, records)
