"""https://adventofcode.com/2023/day/4"""

import re

from ..base import Puzzle


class ScratchCards(Puzzle):

    """Elf scratch card score counting."""

    @staticmethod
    def card_points(row: str) -> int:
        """Calculate number of points awarded from each row."""
        winning, own = [
            {int(i) for i in re.findall(r"(\d+)", s)}
            for s in row.split(":")[1].split("|")
        ]
        matches = own & winning
        score = 2 ** (len(matches) - 1) if len(matches) else 0
        return score

    def part1(self) -> str | int:
        """Calculate total sum of card points in the pile."""
        return sum(self.card_points(row) for row in self.input_text.split("\n") if row)

    def part2(self) -> str | int:
        return ...
