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
        return self.search(start_node=(0,0))

    def part2(self) -> str | int:
        return super().part2()

    def search(self, start_node: tuple[int, int]):
        """Do a breadth-first search for the minimum distance."""
        # queue contains (dist, y, x, dy, dx) tuples
        queue_ = [(0, *start_node, 0, 0)]
        visited = set()
        end_node = (self.shape[0]-1, self.shape[1]-1)

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
                traveled = 0
                for travel_length in range(1, 3+1):
                    new_y = y + dy * travel_length
                    new_x = x + dx * travel_length
                    if (
                        (0 <= new_y <= self.shape[0] - 1)
                        and (0 <= new_x <= self.shape[1] - 1)
                    ):
                        traveled += self.rows[new_y][new_x]
                        # Add here and check visitedness when it comes up in the queue.
                        heapq.heappush(queue_, (dist + traveled, new_y, new_x, dy, dx))