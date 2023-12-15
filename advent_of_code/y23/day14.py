"""https://adventofcode.com/2023/day/14"""

from collections.abc import Iterable
import itertools

from ..base import Puzzle


class ParabolicReflectorDish(Puzzle):

    """A rotating platform containing movable or immovable stones."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.rows = self.input_text.strip().splitlines()

    def position_hash(self) -> int:
        """Returns hash corresponding to the pattern."""
        return hash(self.pattern)

    @property
    def pattern(self) -> str:
        """Get string pattern of the stones."""
        return "\n".join("".join(r) for r in self.rows)

    def pack_north(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards north, pack stones to the top of board."""
        col_iterables = zip(*self.rows)
        cols_packed = map(self.pack_string, col_iterables)
        self.rows = list(zip(*cols_packed))
        return self

    def pack_east(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards east, pack stones to the right of board."""
        self.rows = [self.pack_string(r, reverse=True) for r in self.rows]
        return self

    def pack_south(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards south, pack stones to the bottom of board."""
        col_iterables = zip(*self.rows)
        cols_packed = (self.pack_string(c, reverse=True) for c in col_iterables)
        self.rows = list(zip(*cols_packed))
        return self

    def pack_west(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards west, pack stones to the left of board."""
        self.rows = [self.pack_string(r) for r in self.rows]
        return self

    def pack_cycle(self):
        """Tilt the dish one cycle; pack north, west, south, east."""
        self.pack_north()
        self.pack_west()
        self.pack_south()
        self.pack_east()
        return self

    @classmethod
    def pack_string(cls, original: Iterable[str], reverse=False) -> str:
        """Take original string, pack O characters to beginnings.

        Characters # act as blockers.
        """

        def safe_pack(part: str, reverse: bool) -> str:
            if reverse:
                return "." * part.count(".") + "O" * part.count("O")
            return "O" * part.count("O") + "." * part.count(".")

        start_ = sum(1 for _ in itertools.takewhile(lambda c: c == "#", original))
        ret = start_ * "#"

        while "#" in original[start_:]:
            end2 = original.index("#", start_)
            part = original[start_:end2]
            ret += safe_pack(part, reverse) + "#"
            start_ = end2 + 1

        return ret + safe_pack(original[start_:], reverse)

    def total_load(self) -> int:
        """Calculate total load of the reflector dish."""
        rows = list(self.rows)
        return sum(
            row_no * row.count("O")
            for row, row_no in zip(rows, range(len(rows), 0, -1))
        )

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
