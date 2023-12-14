"""https://adventofcode.com/2023/day/11"""

from dataclasses import dataclass
import itertools

from ..base import Puzzle


class CosmicExpansion(Puzzle):

    """Observe galaxies expanding."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        galaxies = [
            (i, j)
            for i, row in enumerate(self.input_text.strip().splitlines())
            for j, c in enumerate(row)
            if c == "#"
        ]
        self.cosmos = Cosmos(galaxies)

    def expand(self, factor=2) -> "Cosmos":
        """Expand empty rows and columns by given multiplication factor."""
        rows = self.input_text.strip().splitlines()
        empty_rows = [i for i, r in enumerate(rows) if r == "." * len(r)]
        empty_cols = [
            j
            for j in range(len(rows[0]))
            if [rows[i][j] for i in range(len(rows))] == ["."] * len(rows)
        ]

        return self.cosmos.expand(empty_rows, empty_cols, factor)

    def part1(self) -> str | int:
        """Sum of all galaxy distances."""
        expanded = self.expand()
        return sum(expanded.distances())

    def part2(self) -> str | int:
        """Sum of all galaxy distances, given 1e6 expansion factor."""
        expanded = self.expand(1000000)
        return sum(expanded.distances())


@dataclass
class Cosmos:

    """Coordinate space containing galaxies."""

    galaxies: list[tuple[int, int]]

    def expand(self, rows, cols, factor=2) -> "Cosmos":
        """Expand rows and columns by given multiplication factor."""
        ret = [
            (
                gal[0] + (factor - 1) * sum(1 for i in rows if i < gal[0]),
                gal[1] + (factor - 1) * sum(1 for i in cols if i < gal[1]),
            )
            for gal in self.galaxies
        ]

        return Cosmos(ret)

    def distances(self):
        """Calculate manhattan distances between each pair"""
        for g1, g2 in itertools.combinations(self.galaxies, 2):
            yield abs(g2[0] - g1[0]) + abs(g2[1] - g1[1])
