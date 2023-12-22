"""https://adventofcode.com/2023/day/22"""

from collections import namedtuple
import heapq
import itertools
from collections.abc import Iterable
from dataclasses import dataclass

from ..base import Puzzle

@dataclass
class Brick:
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @classmethod
    def from_spec(cls, spec: str) -> "Brick":
        parts = [map(int, pos.split(',')) for pos in spec.split("~")]
        x, y, z = list(zip(*parts))
        return cls(x, y, z)
    
    def __lt__(self, other: "Brick"):
        return self.z[0] < other.z[0]

    def xy_span(self) -> Iterable[tuple[int, int]]:
        yield from itertools.product(
            range(self.x[0], self.x[1]+ 1),
            range(self.y[0], self.y[1]+ 1)
        )

    @property
    def height(self) -> int:
        return self.z[1] - self.z[0] + 1


class SandSlabs(Puzzle):

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.bricks = [Brick.from_spec(s) for s in input_text.strip().splitlines()]
    
    def construct_graph(self):
        brick_dic = {i: brick for i, brick in enumerate(self.bricks)}
        graph = {
            -1: set()
        }

        BlockHeight = namedtuple("BlockHeight", ["z", "block_id"])
        # For each xy cell, order bricks in the order that they would fall
        max_heights: dict[tuple[int, int], BlockHeight] = {}
        for id_, brick in sorted(brick_dic.items(), key=lambda bt: bt[1].z[0]):
            # Find previous max height in the brick xy span
            prev_max = 0
            for xy in brick.xy_span():
                if xy not in max_heights:
                    continue
                if max_heights[xy].z > prev_max:
                    prev_max = max_heights[xy].z
            
            
            # Place this new brick to that current max height
            for xy in brick.xy_span():
                # Create connections to directly supporting bricks
                if prev_max == 0:
                    graph[-1].add(id_)
                elif xy in max_heights and max_heights[xy].z == prev_max:
                    graph[max_heights[xy].block_id].add(id_)

                # Set new max height
                max_heights[xy] = BlockHeight(prev_max + brick.height, id_)

            # Add this block as graph leaf
            graph[id_] = set()

        return graph, brick_dic
    
    @staticmethod
    def reverse_graph(graph: dict):
        ret = {}
        for source, targets in graph.items():
            for target in targets:
                if target not in ret:
                    ret[target] = set()

                ret[target].add(source)
        
        return ret
    
    def can_be_removed(self, graph: dict[int, set[int]]) -> list[int]:
        ret = []
        block_is_supported = self.reverse_graph(graph)
        for node_id, supported_ids in graph.items():
            # Leaves can be removed
            if not supported_ids:
                ret.append(node_id)
                continue

            # Blocks with siblings can be removed
            all_blocks_have_other_supports = True
            for supported_ in supported_ids:
                supporting_blocks = block_is_supported[supported_]
                if len(supporting_blocks) == 1:
                    all_blocks_have_other_supports = False
                    break
            if all_blocks_have_other_supports:
                ret.append(node_id)

        return ret

    def part1(self) -> str | int:
        block_supports, _ = self.construct_graph()
        rem_ids = self.can_be_removed(block_supports)

        return len(rem_ids)
    
    def part2(self) -> str | int:
        return super().part2()
