"""https://adventofcode.com/2023/day/14"""

import itertools

from ..base import Puzzle


class ParabolicReflectorDish(Puzzle):

    """A rotating platform containing movable or immovable stones."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.rows = self.input_text.strip().splitlines()

    @property
    def pattern(self) -> str:
        """Get string pattern of the stones."""
        return '\n'.join(self.rows)
    
    def pack_north(self) -> "ParabolicReflectorDish":
        """Tilt the dish towards north, pack stones to top of board."""
        cols = ["".join(col) for col in zip(*self.rows)]
        cols_packed = [self.pack_string(s) for s in cols]
        self.rows =[''.join(row) for row in zip(*cols_packed)]
        return self

    # def pack_south(self):

    @staticmethod
    def pack_string(original: str) -> str:
        """Take original string, pack O characters to beginnings.
        
        Characters # act as blockers.
        """
        start_ = sum(1 for _ in itertools.takewhile(lambda c: c == "#", original))
        end_ = sum(1 for _ in itertools.takewhile(lambda c: c == "#", reversed(original)))

        ret = start_ * '#' 

        for part in original[start_:len(original)-end_].split("#"):
            # TODO check which is faster: this, or sorted(part, key=order.index(k))
            ret += 'O' * part.count('O') + '.' * part.count('.') + "#"

        return ret[:-1] + end_ * '#'
    
    def total_load(self) -> int:
        """Calculate total load of the reflector dish."""
        return sum(
            row_no * row.count('O')
            for row, row_no in zip(self.rows, range(len(self.rows), 0, -1))
        )

    def part1(self) -> str | int:
        """Tilt platform north, calculate total load."""
        return self.pack_north().total_load()
    
    def part2(self) -> str | int:
        return super().part2()
