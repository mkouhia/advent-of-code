"""https://adventofcode.com/2023/day/21"""

from ..base import Puzzle


class StepCounter(Puzzle):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.rows = self.input_text.strip().splitlines()
        self.shape = (len(self.rows), len(self.rows[0]))
        for i, row in enumerate(self.rows):
            if "S" in row:
                self.start_pos = (i, row.index("S"))

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

                if self.rows[new_y][new_x] == not_allowed:
                    continue

                destinations.add((new_y, new_x))
        return destinations

    def n_loc(self, start_pos: tuple[int, int], n_steps: int):
        locations = {start_pos}
        for _ in range(n_steps):
            locations = self.take_step(locations)
        return len(locations)

    def part1(self) -> str | int:
        return self.n_loc(self.start_pos, 64)

    @classmethod
    def after_n(cls, n) -> tuple[int, int, int, int]:
        ret = {
            "a_even": (n - 1) ** 2,
            "a_odd": n**2,
            "b_": 1,
            "c_": n - 1,
            "d_": n,
        }

        return ret

    def a_cnt(self, n):
        if n == 1:
            return (1, 0)

    def locs_after(self, n_steps):
        dist = self.shape[1]
        dist_h = self.start_pos[1]
        n = n_steps // dist
        assert dist * n + dist_h == n_steps
        assert n >= 1

        n_loc = self.after_n(n)

        offset = 1 - dist_h % 2
        steps = {
            "a_odd": self.n_loc(self.start_pos, dist + (1 - offset)),
            "a_even": self.n_loc(self.start_pos, dist + offset),
            "b_N": self.n_loc((dist, self.start_pos[1]), dist),
            "b_S": self.n_loc((-1, self.start_pos[1]), dist),
            "b_E": self.n_loc((self.start_pos[0], -1), dist),
            "b_W": self.n_loc((self.start_pos[0], dist), dist),
            "d_NE": self.n_loc((dist - 1, -1), dist_h),
            "c_NE": self.n_loc((dist - 1, -1), dist_h + dist),
            "d_SE": self.n_loc((0, -1), dist_h),
            "c_SE": self.n_loc((0, -1), dist_h + dist),
            "d_NW": self.n_loc((dist - 1, dist), dist_h),
            "c_NW": self.n_loc((dist - 1, dist), dist_h + dist),
            "d_SW": self.n_loc((0, dist), dist_h),
            "c_SW": self.n_loc((0, dist), dist_h + dist),
        }

        ret = 0
        for pos in ["a_odd", "a_even"]:
            ret += n_loc[pos] * steps[pos]

        for dir in "NESW":
            ret += n_loc["b_"] * steps[f"b_{dir}"]

        for dir in ["NE", "SE", "SW", "NW"]:
            ret += n_loc["c_"] * steps[f"c_{dir}"]
            ret += n_loc["d_"] * steps[f"d_{dir}"]

        return ret

    def part2(self) -> str | int:
        return self.locs_after(26501365)
