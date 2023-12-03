"""https://adventofcode.com/2023/day/3"""

import re

import numpy as np

from ..helpers import to_numpy_array
from ..base import Puzzle


class GearRatios(Puzzle):

    """Elf ski lift gear ratios."""

    def _extract_numbers(self):
        return {loc: int(num) for loc, num in self._extract_vals(r"\d+").items()}

    def _extract_vals(self, pattern: str) -> dict[tuple[int, int, int], int]:
        """Find out number and their coordinates from input text.

        Args:
            pattern: regex pattern to be found
        Returns:
            Dictionary of coordinate: value, where value is extracted
            number. Coordinates refer to (row, start_x, end_x).
        """
        ret = {}
        for row_i, row in enumerate(self.input_text.splitlines()):
            for match in re.finditer(pattern, row):
                ret[(row_i, match.start(), match.end())] = match.group()
        return ret

    def part_numbers(self):
        """Yields all part numbers in input."""
        background = to_numpy_array(self._separate_background(self.input_text))
        numbers = self._extract_numbers()
        height, width = background.shape

        bg_chars = np.array([" "], dtype="<U1")

        for location, number in numbers.items():
            row, start, end = location
            number_surroundings = background[
                max(row - 1, 0) : min(row + 2, height - 1),
                max(start - 1, 0) : min(end + 1, width - 1),
            ]

            not_background = np.setdiff1d(number_surroundings.ravel(), bg_chars)
            if len(not_background) > 0:
                # The number is connected to some symbol
                yield number

    def gears(self) -> dict[tuple[int, int], tuple[int, int]]:
        """Identify gears.

        Returns:
            Tuples (gear row, gear column): (number 1, number 2)
        """
        canvas = to_numpy_array(self.input_text)
        height, width = canvas.shape

        ret = {}

        gears = self._extract_vals(r"\*")
        for (row, pos, _), _ in gears.items():
            context_array = canvas[max(row - 1, 0) : min(row + 2, height - 1), :].view(
                f"U{width}"
            )
            ctx_rows, _ = context_array.shape

            gear_numbers = []
            for i in range(ctx_rows):
                row_str = context_array[i][0]
                for match in re.finditer(r"\d+", row_str):
                    if match.end() >= pos and match.start() <= pos + 1:
                        gear_numbers.append(int(match.group()))

            if len(gear_numbers) == 2:
                ret[(row, pos)] = tuple(gear_numbers)
            elif len(gear_numbers) >= 2:
                raise UserWarning("Not should have happened")
        return ret

    @staticmethod
    def _separate_background(input_text: str) -> str:
        """Remove numbers and full stops from input text."""
        return re.sub(r"[\d\.]", " ", input_text)

    def part1(self) -> str | int:
        """Returns the sum of part numbers.

        Part numbers are the numbers in the input that are adjacent to
        a symbol.
        """
        return sum(self.part_numbers())

    def part2(self) -> str | int:
        """Returns the sum of gear ratios.

        Gears are '*' symbols in the input text, gear ratio is produced
        by multiplying numbers adjacent to gears.
        """
        return sum(np.prod(i) for i in self.gears().values())
