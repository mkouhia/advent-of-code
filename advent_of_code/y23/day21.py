"""https://adventofcode.com/2023/day/21"""

from ..base import Puzzle


class StepCounter(Puzzle):
    def __init__(self, input_text: str, n_steps=64) -> None:
        super().__init__(input_text)
        self.rows = self.input_text.strip().splitlines()
        self.shape = (len(self.rows), len(self.rows[0]))
        for i, row in enumerate(self.rows):
            if "S" in row:
                self.start_pos = (i, row.index("S"))
        self.n_steps = n_steps

    def take_step(self, locations: set[tuple[int, int]], not_allowed="#"):
        destinations = set()
        for loc in locations:
            for dy, dx in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_y = loc[0] + dy
                new_x = loc[1] + dx

                if not (
                    (0 <= new_y <= self.shape[0] - 1)
                    and (0 <= new_x <= self.shape[1] - 1)
                ):
                    continue

                if self.rows[new_y][new_x] in not_allowed:
                    continue

                destinations.add((new_y, new_x))
        return destinations

    def part1(self) -> str | int:
        locations = {self.start_pos}
        for _ in range(self.n_steps):
            locations = self.take_step(locations)
        return len(locations)

    def part2(self) -> str | int:
        return super().part2()
