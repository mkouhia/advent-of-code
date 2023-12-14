"""https://adventofcode.com/2023/day/10"""

from collections.abc import Iterator

import matplotlib.path

from ..base import Puzzle


class PipeMaze(Puzzle, Iterator):

    """Maze that consists of ascii characters."""

    plumbing = ["|", "-", "L", "J", "7", "F"]

    possible_movements = {
        (-1, 0): {
            "|": (-1, 0),
            "F": (0, 1),
            "7": (0, -1),
        },
        (0, 1): {
            "-": (0, 1),
            "7": (1, 0),
            "J": (-1, 0),
        },
        (1, 0): {
            "|": (1, 0),
            "L": (0, 1),
            "J": (0, -1),
        },
        (0, -1): {
            "-": (0, -1),
            "L": (-1, 0),
            "F": (1, 0),
        },
    }

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.maze = input_text.strip().splitlines()
        self._pos = None
        self._dir: tuple[int, int] = None
        self.shape = (len(self.maze), len(self.maze[0]))

    def __next__(self):
        if self._pos is None:
            for i, line in enumerate(self.maze):
                if "S" in line:
                    self._pos = (i, line.index("S"))
            self._dir = self._look_around()
            return self._pos

        next_pos = (self._pos[0] + self._dir[0], self._pos[1] + self._dir[1])
        next_char = self.maze[next_pos[0]][next_pos[1]]
        if next_char == "S":
            raise StopIteration
        next_dir = self.possible_movements[self._dir][next_char]

        self._dir = next_dir
        self._pos = next_pos
        return self._pos

    def _look_around(self):
        """Look for possible movements at start position."""
        for (dy, dx), allowed_dict in self.possible_movements.items():
            next_y = self._pos[0] + dy
            next_x = self._pos[1] + dx
            if (
                next_y < 0
                or next_y >= self.shape[0]
                or next_x < 0
                or next_x >= self.shape[1]
            ):
                continue  # Not inside maze
            if self.maze[next_y][next_x] in allowed_dict:
                # Go this way
                return (dy, dx)
        raise UserWarning(f"Cannot go anywhere around {self._pos}")

    def part1(self) -> str | int:
        """Number of steps from the start from the farthest position."""
        return len(list(self)) // 2

    def part2(self) -> str | int:
        """Number of points inside this polygon.

        Employ Matplotlib functionality. Manual crossing count ended up
        too tedious.

        See also https://stackoverflow.com/q/36399381
        """
        edge_pts = list(self)

        polygon = matplotlib.path.Path(
            [p for p in edge_pts if self._char(*p) not in "-|"] + [edge_pts[0]],
            closed=True,
        )

        points_within = 0
        for i in range(self.shape[0]):
            edge_j = sorted(p[1] for p in edge_pts if p[0] == i)

            # Do not investigate points that are definitely not inside the polygon
            if len(edge_j) == 0:
                continue

            for j in range(min(edge_j), max(edge_j) + 1):
                if (i, j) in edge_pts:
                    continue

                if polygon.contains_point((i, j)):
                    points_within += 1

        return points_within

    def _char(self, i, j):
        return self.maze[i][j]
