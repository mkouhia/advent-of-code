"""https://adventofcode.com/2023/day/8"""

import itertools
import math
import re

from ..base import Puzzle


class HauntedWasteland(Puzzle):

    """Navigate away from the wasteland.

    An elf has provided us with a map representing nodes. How to find
    ourselves out from the desert?
    """

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        rows = input_text.strip().splitlines()
        self.directions = [0 if i == "L" else 1 for i in rows[0]]

        pattern = re.compile(r"(\w+) = \((\w+), (\w+)\)")
        self.nodes = {
            node[0]: (node[1], node[2])
            for spec in rows[2:]
            if (node := pattern.search(spec).groups())
        }

    def get_iter_count(self, directions, start, end_re):
        """Find iteration count to get from the start to the end."""
        node_ = start
        count = 0
        while not re.match(end_re, node_) or count == 0:
            count += 1
            dir_ = next(directions)
            node_ = self.nodes[node_][dir_]
        return node_, count

    def part1(self) -> str | int:
        """Navigate to the end of the map."""
        directions = itertools.cycle(self.directions)
        _, count = self.get_iter_count(directions, "AAA", "ZZZ")
        return count

    def part2(self) -> str | int:
        """Find count by examining different loop lengths.

        Brute-forcing does not work. It appears that the loops will be
        endless, repeating the same number pattern. Hence, least common
        multiple will serve the solution.
        """
        nodes_ = [n for n in self.nodes if n.endswith("A")]
        loops = []

        for n in nodes_:
            directions = itertools.cycle(self.directions)
            endpoints = []
            start_ = n
            for _ in range(2):
                node_, count = self.get_iter_count(directions, start_, "..Z")
                endpoints.append((node_, count))
            assert endpoints[0] == endpoints[1], "No complex looping"
            loops.append(endpoints[0][1])

        return math.lcm(*loops)
