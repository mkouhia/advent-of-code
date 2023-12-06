"""https://adventofcode.com/2023/day/6"""

import re
from dataclasses import dataclass
from math import ceil, floor, sqrt

from ..base import Puzzle


class WaitForIt(Puzzle):

    """Race calculator for elf toy boat races."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.races = None

    def part1(self) -> str | int:
        """Find out, how many winning combinations there are."""
        times, distances = [
            [int(i) for i in re.findall(r"\d+", row)]
            for row in self.input_text.strip().split("\n")
        ]
        self.races = [Race(*i) for i in list(zip(times, distances))]

        return self.ways_to_beat()

    def part2(self) -> str | int:
        """Same as part1, but all numbers map to one game."""
        time, distance = [
            int("".join(re.findall(r"\d+", row)))
            for row in self.input_text.strip().split("\n")
        ]
        self.races = [Race(time, distance)]

        return self.ways_to_beat()

    def ways_to_beat(self) -> int:
        """Returns the number of distinct ways a race can be won."""
        total = 1
        for race in self.races:
            total *= race.ways_to_beat()
        return total


@dataclass
class Race:

    """Toy boat race"""

    time: int
    distance: int

    def travel(self, t_charge: int, dv=1):
        """How far a boat will travel, given time to charge."""
        return dv * t_charge * (self.time - t_charge)

    def ways_to_beat(self, dv=1) -> int:
        """Number of ways, in which the race can be beaten."""
        roots = sorted(
            [
                (
                    -(self.time * dv)
                    + k * sqrt((self.time * dv) ** 2 - 4 * (-1) * (-self.distance))
                )
                / 2
                * (-1)
                for k in [1, -1]
            ]
        )
        return ceil(roots[-1] - 1) + 1 - floor(roots[0] + 1)
