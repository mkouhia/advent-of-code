"""Abstract base class for a day's advent calendar solution."""

from abc import ABC, abstractmethod


class Puzzle(ABC):
    """Base class for puzzle solutions."""

    def __init__(self, input_text: str) -> None:
        self.input_text = input_text

    @abstractmethod
    def part1(self) -> str | int:
        """Returns puzzle solution to part 1."""
        raise NotImplementedError

    @abstractmethod
    def part2(self) -> str | int:
        """Returns puzzle solution to part 1."""
        raise NotImplementedError
