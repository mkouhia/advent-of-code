"""https://adventofcode.com/2023/day/9"""

import numpy as np
from ..base import Puzzle


class MirageMaintenance(Puzzle):

    """Predict OASIS sensor values."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.histories = [
            np.array([int(i) for i in row.split(" ")])
            for row in input_text.strip().splitlines()
        ]

    @staticmethod
    def row_history(row: np.ndarray, record_idx=-1) -> list[int]:
        """Get last or first values of row differences."""
        record_values = []
        stage = row
        while not np.all(stage == 0):
            record_values.append(stage[record_idx])
            stage = stage[1:] - stage[:-1]
        return record_values

    @classmethod
    def predict_last(cls, row) -> int:
        """Predict last value for measurement history"""
        return sum(cls.row_history(row, -1))

    @classmethod
    def predict_first(cls, row) -> int:
        """Predict first value for measurement history"""
        first_values = cls.row_history(row, 0)
        res = None
        for val in first_values[::-1]:
            res = val if res is None else val - res
        return res

    def part1(self) -> str | int:
        """Sum of extrapolated last values."""
        return sum(self.predict_last(row) for row in self.histories)

    def part2(self) -> str | int:
        """Sum of extrapolated first values."""
        return sum(self.predict_first(row) for row in self.histories)
