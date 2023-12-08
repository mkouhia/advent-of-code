"""https://adventofcode.com/2021/day/6"""

from collections.abc import Iterator
from ..base import Puzzle


class Lanternfish(Puzzle):

    """Lanternfish in the sea."""

    def part1(self) -> str | int:
        kalat = LanternfishShoal.from_string(80, self.input_text.strip())
        return list(kalat)[-1]

    def part2(self) -> str | int:
        kalat = LanternfishShoal.from_string(256, self.input_text.strip())
        return list(kalat)[-1]


class LanternfishShoal(Iterator):

    """A shoal of lanternfish.

    As per the instructions, the fish reproduce every 7 days, and the
    new hatchlings will take 9 days to produce their first offspring.
    """

    def __init__(self, days: int, **timers):
        self.days = days
        self.timer_count = {i: 0 for i in range(9)} | {
            int(i): cnt for i, cnt in timers.items()
        }
        self._step = 0

    @classmethod
    def from_string(cls, days, timer_str: str):
        """Create fish from comma-separated list of timer values."""
        timers = {str(i): 0 for i in range(9)}
        for i in timer_str.split(","):
            timers[i] += 1
        return cls(days, **timers)

    def __next__(self):
        self.timer_count = {t - 1: cnt for t, cnt in self.timer_count.items()}
        reproduce_cnt = self.timer_count.pop(-1)
        self.timer_count[8] = reproduce_cnt  # new fish
        self.timer_count[6] += reproduce_cnt  # reset timer for old fish

        if self._step == self.days:
            raise StopIteration
        self._step += 1

        return sum(self.timer_count.values())
