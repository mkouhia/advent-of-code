"""https://adventofcode.com/2023/day/13"""

from collections.abc import Iterable

from ..base import Puzzle


class PointOfIncidence(Puzzle):

    """Mirror maze on Lava Island."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.patterns = [
            Pattern(pat_txt) for pat_txt in self.input_text.strip().split("\n\n")
        ]

    def part1(self) -> str | int:
        """Sum of pattern values."""
        return sum(p.mirror_value() for p in self.patterns)

    def part2(self) -> str | int:
        """Sum of pattern values.

        Find mirror values that have number of faults equal to 1.
        """
        return sum(p.mirror_value(num_faults=1) for p in self.patterns)


class Pattern:

    """Mirror pattern."""

    def __init__(self, text) -> None:
        self.text = text
        self.row_strings = text.splitlines()
        self.col_strings = ["".join(col) for col in zip(*self.row_strings)]

    def mirror_value(self, num_faults=0):
        """Calculate the mirror value of this pattern.

        Assume that one pattern has either horizontal or vertical mirroring,
        not both.
        """
        if val := self._mirror_row(num_faults):
            return 100 * val
        return self._mirror_col(num_faults)

    def _mirror_col(self, num_faults=0):
        return mirror_point(self.col_strings, num_faults)

    def _mirror_row(self, num_faults=0):
        return mirror_point(self.row_strings, num_faults)


def mirror_point(elements: Iterable, num_faults=0):
    """Calculate the point in elements, where the iterable is mirrored."""
    break_order = sorted(
        range(1, len(elements)), key=lambda k: abs(len(elements) / 2 - k)
    )
    for breakpoint in break_order:
        if _num_faults(elements, breakpoint) == num_faults:
            return breakpoint
    return 0


def _num_faults(it: list[str], point: int) -> tuple[int, int]:
    """Number of faults in each mirrored pattern.
    
    Args:
        it: List of strings to be matched.
        point: Index of mirroring point.
    """
    elements = zip(it[:point][::-1], it[point:])
    return sum(
        map(lambda p: sum(map(lambda q: q[0] != q[1], zip(p[0], p[1]))), elements)
    )
