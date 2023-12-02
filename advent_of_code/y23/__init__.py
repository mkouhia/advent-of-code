"""Functions for Advent of Code 2023."""

from ..base import Puzzle
from .day01 import Trebuchet
from .day02 import CubeConundrum

solutions: dict[int, Puzzle] = {
    1: Trebuchet,
    2: CubeConundrum,
}
