"""https://adventofcode.com/2023/day/3"""

import re

import numpy as np

from ..helpers import to_numpy_array
from ..base import Puzzle


class GearRatios(Puzzle):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)

    def extract_numbers(self) -> dict[tuple[int, int, int], int]:
        """Find out number and their coordinates from input text.

        Returns:
            Dictionary of coordinate: value, where value is extracted
            number. Coordinates refer to (row, start_x, end_x).
        """
        ret = {}
        for row_i, row in enumerate(self.input_text.splitlines()):
            start_j = None
            pending = ""
            for char_j, char_ in enumerate(row):
                if char_ in "0123456789":
                    if not pending:
                        start_j = char_j
                    pending += char_
                elif pending:
                    # Finalize pending number
                    ret[(row_i, start_j, char_j)] = int(pending)
                    pending = ""

            # Check end of row condition
            if pending:
                ret[(row_i, start_j, char_j)] = int(pending)
                pending = ""

        return ret

    def part_numbers(self):
        """Yields all part numbers in input."""
        print(self.input_text)
        background = to_numpy_array(self._separate_background(self.input_text))
        numbers = self.extract_numbers()
        height, width = background.shape

        bg_chars = np.array([" "], dtype="<U1")

        for location, number in numbers.items():
            row, start, end = location
            number_surroundings = background[
                max(row - 1, 0) : min(row + 2, height - 1),
                max(start - 1, 0) : min(end + 1, width - 1),
            ]

            print(number)
            print(number_surroundings)

            not_background = np.setdiff1d(number_surroundings.ravel(), bg_chars)
            if len(not_background) > 0:
                # The number is connected to some symbol
                yield number

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
        return super().part2()
