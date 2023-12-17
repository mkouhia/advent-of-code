"""https://adventofcode.com/2023/day/17"""

import itertools
import sys
from typing import TypeVar

from tqdm import tqdm

from ..base import Puzzle


class ClumsyCrucible(Puzzle):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.rows = input_text.strip().split("\n")
        self.shape = (len(self.rows), len(self.rows[0]))

    def part1(self) -> str | int:
        """Least heat loss on the crucible path."""
        graph = self.construct_graph()
        dist, _ = dijkstra_algorithm(graph, (0, 0), progress=True)
        return min(dist[(self.shape[0] - 1, self.shape[1] - 1)].values())

    def part2(self) -> str | int:
        return super().part2()

    def construct_graph(
        self,
    ) -> dict[tuple[int, int], list[tuple[tuple[int, int], int]]]:
        """Construct graph from puzzle rectangular input."""
        graph = {}
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                graph[(row, col)] = self.neighbours(row, col)
        return graph

    def neighbours(self, i, j) -> list[tuple[tuple[int, int], int]]:
        """Construct list of neighboring nodes to (i, j).

        Returns list of node, distance, direction tuples.
        """
        neighbours = []
        for dy, dx, s in [(0, -1, "<"), (0, 1, ">"), (-1, 0, "^"), (1, 0, "v")]:
            if (0 <= (ny := i + dy) <= self.shape[0] - 1) and (
                0 <= (nx := j + dx) <= self.shape[1] - 1
            ):
                node = (ny, nx)
                weight = self.rows[node[0]][node[1]]
                neighbours.append((node, int(weight), s))
        return neighbours


T = TypeVar("T")


def dijkstra_algorithm(
    graph: dict[T, list[tuple[T, int]]], start_node: T, progress=False
):
    queue_ = set(graph.keys())

    # Node: {'ddd': dist} where d are previous directions
    dist = {start_node: {"": 0}}
    prev = {}

    pbar = tqdm(total=len(queue_)) if progress else None
    while queue_:
        # u ← vertex in Q with min dist[u]
        # remove u from Q
        current_min_node = next(
            node_
            for node_, _ in sorted(dist.items(), key=lambda p: min(p[1].values()))
            if node_ in queue_
        )
        queue_.remove(current_min_node)

        # for each neighbor v of u still in Q
        # TODO here, possible neighbours are those that allow shift into that dir
        neighbors = graph[current_min_node]
        for neighbor, weight, dir_ in neighbors:
            # Go through different ways that current node was reached
            for path_hist, cur_dist in dist[current_min_node].items():
                if path_hist == dir_ * 3:
                    continue  # Cannot continue this direction
                if len(path_hist) > 0 and "".join(sorted([path_hist[0], dir_])) in [
                    "<>",
                    "^v",
                ]:
                    continue  # Do not cycle back and forth

                new_hist = (
                    "".join(itertools.takewhile(lambda k: k == dir_, path_hist[::-1]))
                    + dir_
                )

                # if neighbor not in queue_:
                #     continue
                tentative_value = cur_dist + weight
                if neighbor not in dist:
                    dist[neighbor] = {}
                if tentative_value < dist[neighbor].get(new_hist, sys.maxsize):
                    dist[neighbor][new_hist] = tentative_value
                    # We also update the best path to the current node
                    prev[neighbor] = current_min_node

        if progress:
            pbar.update()

    return dist, prev
