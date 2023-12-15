"""https://adventofcode.com/2023/day/14"""

from collections.abc import Iterable
from enum import Enum
from functools import cache, cached_property
import itertools

import numpy as np

from ..base import Puzzle
from ..helpers import char_array_to_string, to_numpy_array


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


class ParabolicReflectorDish(Puzzle):

    """A rotating platform containing movable or immovable stones."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        arr = to_numpy_array(self.input_text, 'S')
        self.movable = arr == b'O'
        self.immovable = arr == b'#'
        self.shape = arr.shape

    def position_hash(self) -> int:
        """Returns hash corresponding to the pattern."""
        return hash(self.movable.tobytes())
    
    @property
    def pattern(self):
        """Get string pattern of the stones."""
        arr = np.full_like(self.immovable, b'.', dtype='S1')
        arr[self.immovable] = b'#'
        arr[self.movable] = b'O'
        print(arr.shape)
        return char_array_to_string(arr)

    def pack_north(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards north, pack stones to the top of board."""
        for span_ in self.spans_vertical:
            self.movable[span_] = ~np.sort(~self.movable[span_])
        return self

    def pack_east(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards east, pack stones to the right of board."""
        for span_ in self.spans_horizontal:
            self.movable[span_] = np.sort(self.movable[span_])
        return self

    def pack_south(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards south, pack stones to the bottom of board."""
        for span_ in self.spans_vertical:
            self.movable[span_] = np.sort(self.movable[span_])
        return self

    def pack_west(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards west, pack stones to the left of board."""
        for span_ in self.spans_horizontal:
            self.movable[span_] = ~np.sort(~self.movable[span_])
        return self
        
    @cached_property
    def spans_horizontal(self):
        """Free places between fixed stones, in horizontal direction"""
        ret = []
        blocks = np.nonzero(self.immovable)
        for i in range(self.shape[0]):
            row_breaks = blocks[1][blocks[0] == i].tolist()
            breaks = [-1] + row_breaks + [self.shape[1]]
            for pair in itertools.pairwise(breaks):
                if (start_ := pair[0] + 1) == pair[1]:
                    continue
                ret.append(np.s_[i, start_:pair[1]])
        
        return ret

    @cached_property
    def spans_vertical(self):
        """Free places between fixed stones, in vertical direction"""
        ret = []
        blocks = np.nonzero(self.immovable)
        order_ = np.argsort(blocks[1])
        blocks = [blocks[i][order_] for i in [0, 1]]


        for i in range(self.shape[1]):
            col_breaks = np.sort(blocks[0][blocks[1] == i]).tolist()
            breaks = [-1] + col_breaks + [self.shape[0]]
            for pair in itertools.pairwise(breaks):
                if (start_ := pair[0] + 1) == pair[1]:
                    continue
                ret.append(np.s_[start_:pair[1], i])
        
        return ret

    def pack_cycle(self):
        """Tilt the dish one cycle; pack north, west, south, east."""
        self.pack_north()
        self.pack_west()
        self.pack_south()
        self.pack_east()
        return self

    def total_load(self) -> int:
        """Calculate total load of the reflector dish."""
        return np.sum(self.movable.sum(axis=1) * np.arange(self.shape[0], 0, -1))

    def part1(self) -> str | int:
        """Tilt platform north, calculate total load."""
        return self.pack_north().total_load()

    def part2(self) -> str | int:
        """Find total load after 1e9 cycles."""
        hashes = []
        weights = []
        base_cycles = 0
        cycle_modulo = 0
        while not cycle_modulo:
            hash_ = self.position_hash()
            if hash_ in hashes:
                base_cycles = hashes.index(hash_)
                cycle_modulo = len(hashes) - base_cycles
                break
            weights.append(self.total_load())
            hashes.append(hash_)

            self.pack_cycle()

        idx = int((1e9 - base_cycles) % cycle_modulo + base_cycles)
        return weights[idx]
