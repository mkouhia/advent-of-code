"""https://adventofcode.com/2023/day/4"""

import re

import numpy as np

from ..base import Puzzle


class ScratchCards(Puzzle):

    """Elf scratch card score counting."""

    @staticmethod
    def card_matches(row: str) -> int:
        """Calculate amount of matching numbers on each row"""
        winning, own = [
            {int(i) for i in re.findall(r"(\d+)", s)}
            for s in row.split(":")[1].split("|")
        ]
        matches = own & winning
        return len(matches)

    @classmethod
    def card_points(cls, row: str) -> int:
        """Calculate number of points awarded from each row."""
        matches = cls.card_matches(row)
        return 2 ** (matches - 1) if matches else 0

    def part1(self) -> str | int:
        """Calculate total sum of card points in the pile."""
        return sum(self.card_points(row) for row in self.input_text.split("\n") if row)

    def part2(self) -> str | int:
        """Calculate total amount of scratchcards in the end."""
        card_matches = [
            self.card_matches(row) for row in self.input_text.split("\n") if row
        ]
        card_amounts = np.ones_like(card_matches, dtype=int)
        for i, num in enumerate(card_matches):
            card_amounts[i + 1 : i + 1 + num] += card_amounts[i]
        return np.sum(card_amounts)
