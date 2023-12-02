"""https://adventofcode.com/2023/day/2"""

import re
from dataclasses import dataclass

from ..base import Puzzle


class CubeConundrum(Puzzle):

    """Analyze game statistics, return possible games."""

    @classmethod
    def solve(cls, input_text: str) -> str:
        """Returns the sum of IDs for games that were possible."""
        games = cls.parse_games(input_text)
        return sum(g.id for g in games if g.is_possible(red=12, green=13, blue=14))

    @staticmethod
    def parse_games(spec: str):
        return [Game.from_record(row) for row in spec.splitlines()]


@dataclass
class Reveal:
    """Game round: reveal of cubes."""

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


class Game:
    def __init__(self, id: int, reveals: list[Reveal] = None) -> None:
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

    @classmethod
    def from_record(cls, record: str):
        game_str, record_list = record.split(":")
        id_match = re.search(r"Game (\d+)", game_str)
        id = int(id_match.group(1))
        records = [Reveal.from_string(i) for i in record_list.split(";")]

        return cls(id, records)
