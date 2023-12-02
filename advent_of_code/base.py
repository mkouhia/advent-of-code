"""Abstract base class for a day's advent calendar solution."""

from abc import ABC, abstractclassmethod


class Puzzle(ABC):
    """Base class for puzzle solutions."""

    @abstractclassmethod
    def part1(cls, input_text: str) -> str | int:
        """Returns puzzle solution to part 1."""
        ...

    @abstractclassmethod
    def part2(cls, input_text: str) -> str | int:
        """Returns puzzle solution to part 1."""
        ...
