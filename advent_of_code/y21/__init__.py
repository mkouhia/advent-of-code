"""Functions for Advent of Code 2021."""

from ..base import Puzzle
from .day06 import Lanternfish
from .day19 import BeaconScanner


solutions: dict[int, Puzzle] = {
    6: Lanternfish,
    19: BeaconScanner,
}
