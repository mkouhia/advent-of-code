"""https://adventofcode.com/2023/day/16"""

import itertools
from ..base import Puzzle


class Beam:

    """Beam of light, going into some direction

    Attrs:
        y: Location of beam head, row.
        x: Location of beam head, column.
        dir: Direction where beam head is pointing, enum of unit circle.
    """

    _dirs = {
        0: (0, 1),
        1: (-1, 0),
        2: (0, -1),
        3: (1, 0),
    }

    def __init__(self, y, x, dir_):
        self.y = y
        self.x = x
        self.dir = dir_

    def __repr__(self) -> str:
        return f"<Beam y={self.y}, x={self.x}, dir={self.dir}>"

    def advance(self):
        """Go forward one time step."""
        dy, dx = self._dirs[self.dir]
        self.y += dy
        self.x += dx

    def split(self):
        """Split beam in two.

        Modify direction of the original, return other beam.
        """
        old_dir = self.dir
        self.dir = (self.dir + 1) % 4
        return Beam(self.y, self.x, (old_dir - 1) % 4)

    def turn_right(self):
        """Turn right."""
        self.dir = (self.dir - 1) % 4

    def turn_left(self):
        """Turn left."""
        self.dir = (self.dir + 1) % 4

    def as_tuple(self):
        """Return x,y,dir as tuple."""
        return (self.x, self.y, self.dir)


class TheFloorWillBeLava(Puzzle):

    """Beam reflection in a contraption."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.rows = input_text.strip().splitlines()
        self.shape = (len(self.rows), len(self.rows[0]))
        self.setup()

    def setup(self, beam=None):
        """Reset with initial beam."""
        self.energized = [
            [False for _ in range(self.shape[1])] for _ in range(self.shape[0])
        ]
        self.beams = [beam] if beam is not None else []
        self.history = set()
        self.time = -1

    def step(self):
        """Proceed to next time step."""
        new_beams = []
        for beam in self.beams:
            cur_char = self.rows[beam.y][beam.x] if self.time >= 0 else "."

            other_beam = None
            if cur_char == "|" and beam.dir in [0, 2]:
                other_beam = beam.split()
            elif cur_char == "-" and beam.dir in [1, 3]:
                other_beam = beam.split()
            elif cur_char == "\\" and beam.dir in [0, 2]:
                beam.turn_right()
            elif cur_char == "\\" and beam.dir in [1, 3]:
                beam.turn_left()
            elif cur_char == "/" and beam.dir in [0, 2]:
                beam.turn_left()
            elif cur_char == "/" and beam.dir in [1, 3]:
                beam.turn_right()

            beam.advance()
            if other_beam is not None:
                other_beam.advance()
                new_beams.append(other_beam)

        filtered_beams = []
        for beam in self.beams + new_beams:
            if (tup := beam.as_tuple()) in self.history:
                continue
            self.history.add(tup)

            if not 0 <= beam.y < self.shape[0]:
                continue
            if not 0 <= beam.x < self.shape[1]:
                continue

            filtered_beams.append(beam)
            self.energized[beam.y][beam.x] = True

        self.beams.clear()
        self.beams.extend(filtered_beams)

        self.time += 1

    def _max_energized(self, beam=None):
        self.setup(beam or Beam(0, -1, 0))
        while len(self.beams) > 0:
            self.step()
        return sum(1 for row in self.energized for cell in row if cell)

    def part1(self) -> str | int:
        """Returns total number of energized cells at the end."""
        return self._max_energized()

    def part2(self) -> str | int:
        """Maximum energization value, beam from any direction."""
        max_val = 0
        for dir_ in range(4):
            if dir_ in [0, 2]:
                y = range(self.shape[0])
                x = [-1] if dir_ == 0 else [self.shape[1]]
            else:
                y = [-1] if dir_ == 3 else [self.shape[0]]
                x = range(self.shape[1])

            for y_, x_ in itertools.product(y, x):
                beam = Beam(y_, x_, dir_)
                if (value := self._max_energized(beam)) > max_val:
                    max_val = value
        return max_val
