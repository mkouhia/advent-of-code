"""https://adventofcode.com/2023/day/17"""

import sys
from collections import defaultdict
from typing import Any, TypeVar

from ..base import Puzzle

class ClumsyCrucible(Puzzle):
    
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.rows = input_text.strip().split('\n')
        self.shape = (len(self.rows), len(self.rows[0]))
    
    def part1(self) -> str | int:
        """Least heat loss on the crucible path."""
        graph = self.construct_graph()
        dist, _ = dijkstra_algorithm(graph, (0,0))
        return dist[(self.shape[0] - 1, self.shape[1] - 1)]
    
    def part2(self) -> str | int:
        return super().part2()
    
    def construct_graph(self) -> dict[tuple[int, int], list[tuple[tuple[int, int], int]]]:
        """Construct graph from puzzle rectangular input."""
        graph = {}
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                graph[(row, col)] = self.neighbours(row, col)
        return graph
                
    def neighbours(self, i, j) -> list[tuple[tuple[int, int], int]]:
        """Construct list of neighboring nodes to (i, j).
        
        Returns list of node, distance pairs.
        """
        neighbours = []
        for dy, dx in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if (
                (0 <= (ny := i+dy) <= self.shape[0]-1)
                and (0 <= (nx := j+dx) <= self.shape[1] - 1)
            ):
                node = (ny, nx)
                weight = self.rows[node[0]][node[1]]
                neighbours.append((node, int(weight)))
        return neighbours
                    


T = TypeVar("T")
def dijkstra_algorithm(graph: dict[T, list[tuple[T, int]]], start_node: T):
    queue_ = set(graph.keys())
 
    dist = {start_node: 0}
    prev = {}
    
    while queue_:
        # u ← vertex in Q with min dist[u]
        # remove u from Q
        current_min_node = next(
            node_ for node_, _ in sorted(dist.items(), key=lambda p: p[1])
            if node_ in queue_
        )
        queue_.remove(current_min_node)

        # for each neighbor v of u still in Q
        # TODO here, possible neighbours are those that allow shift into that dir
        neighbors = graph[current_min_node]
        for neighbor, weight in neighbors:
            # if neighbor not in queue_:
            #     continue
            tentative_value = dist.get(current_min_node, sys.maxsize) + weight
            if tentative_value < dist.get(neighbor, sys.maxsize):
                dist[neighbor] = tentative_value
                # We also update the best path to the current node
                prev[neighbor] = current_min_node
 
    
    return dist, prev