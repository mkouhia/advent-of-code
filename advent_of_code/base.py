"""Abstract base class for a day's advent calendar solution."""

from abc import ABC, abstractclassmethod


class Puzzle(ABC):
    """Base class for puzzle solutions."""

    @abstractclassmethod
    def solve(cls, input_text: str) -> str:
        """Returns puzzle solution, given a certain input text."""
        ...
