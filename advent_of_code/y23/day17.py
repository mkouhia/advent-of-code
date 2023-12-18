"""https://adventofcode.com/2023/day/17"""

import heapq

from ..base import Puzzle


class ClumsyCrucible(Puzzle):

    """Breadth-first search (BFS) for 2d array navigation.

    Each cell has an entry cost, and the legs must be of certain length.
    Therefore, basic Dijkstra's algorithm does not apply.
    """

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.rows = [[int(c) for c in row] for row in input_text.strip().split("\n")]
        self.shape = (len(self.rows), len(self.rows[0]))

    def part1(self) -> str | int:
        """Least heat loss on the crucible path."""
        return self.search_bfs(start_node=(0, 0), max_leg=3)

    def part2(self) -> str | int:
        return self.search_bfs(start_node=(0, 0), min_leg=4, max_leg=10)

    def search_bfs(self, start_node: tuple[int, int], min_leg=1, max_leg=3):
        """Do a breadth-first search for the minimum distance.

        Heapq provides priority queue algorithm, which makes insertion
        and taking smallest element quite cheap.

        https://docs.python.org/3/library/heapq.html
        """
        # queue contains (dist, y, x, dy, dx) tuples
        queue_ = [(0, *start_node, 0, 0)]
        visited = set()
        end_node = (self.shape[0] - 1, self.shape[1] - 1)

        while queue_:
            dist, y, x, dy_prev, dx_prev = heapq.heappop(queue_)

            if (y, x) == end_node:
                return dist
            if (cur_pt := (y, x, dy_prev, dx_prev)) in visited:
                continue

            visited.add(cur_pt)

            # Next possible directions, 0..3 steps to some other direction
            for dy, dx in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                if (dy, dx) in [(dy_prev, dx_prev), (-dy_prev, -dx_prev)]:
                    continue
                traveled = dist
                for travel_length in range(1, max_leg + 1):
                    new_y = y + dy * travel_length
                    new_x = x + dx * travel_length

                    if not (
                        (0 <= new_y <= self.shape[0] - 1)
                        and (0 <= new_x <= self.shape[1] - 1)
                    ):
                        break

                    traveled += self.rows[new_y][new_x]
                    if travel_length < min_leg:
                        continue

                    # Add here and check visitedness when it comes up in the queue.
                    heapq.heappush(queue_, (traveled, new_y, new_x, dy, dx))
