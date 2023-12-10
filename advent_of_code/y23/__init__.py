"""Functions for Advent of Code 2023."""

from ..base import Puzzle
from .day01 import Trebuchet
from .day02 import CubeConundrum
from .day03 import GearRatios
from .day04 import ScratchCards
from .day05 import Almanac
from .day06 import WaitForIt
from .day07 import CamelCards
from .day08 import HauntedWasteland
from .day09 import MirageMaintenance
from .day10 import PipeMaze


solutions: dict[int, Puzzle] = {
    1: Trebuchet,
    2: CubeConundrum,
    3: GearRatios,
    4: ScratchCards,
    5: Almanac,
    6: WaitForIt,
    7: CamelCards,
    8: HauntedWasteland,
    9: MirageMaintenance,
    10: PipeMaze,
}
