"""https://adventofcode.com/2023/day/22"""

from collections import deque, namedtuple
import itertools
from collections.abc import Iterable
from dataclasses import dataclass

from ..base import Puzzle


@dataclass
class Brick:
    """A rectangular brick taking some amount of x,y,z space."""

    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @classmethod
    def from_spec(cls, spec: str) -> "Brick":
        parts = [map(int, pos.split(",")) for pos in spec.split("~")]
        x, y, z = list(zip(*parts))
        return cls(x, y, z)

    def __lt__(self, other: "Brick"):
        return self.z[0] < other.z[0]

    def xy_span(self) -> Iterable[tuple[int, int]]:
        yield from itertools.product(
            range(self.x[0], self.x[1] + 1), range(self.y[0], self.y[1] + 1)
        )

    @property
    def height(self) -> int:
        """Height in z direction"""
        return self.z[1] - self.z[0] + 1


class SandSlabs(Puzzle):

    """Graph traversal problem, given 3d blocks."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.bricks = [Brick.from_spec(s) for s in input_text.strip().splitlines()]
        self.support_graph, self.brick_dic = self.construct_graph()
        self.depend_graph = self.reverse_graph(self.support_graph)

    def construct_graph(self):
        """Create graph: brick -> bricks supported by this brick."""
        brick_dic = {i: brick for i, brick in enumerate(self.bricks)}
        graph = {-1: set()}

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
    def reverse_graph(graph: dict[int, set[int]]) -> dict[int, set[int]]:
        """Reverse graph - returns: brick -> bricks that support this brick."""
        ret = {}
        for source, targets in graph.items():
            for target in targets:
                if target not in ret:
                    ret[target] = set()

                ret[target].add(source)

        return ret

    def can_be_removed(self) -> list[int]:
        ret = []
        for node_id, supported_ids in self.support_graph.items():
            # Leaves can be removed
            if not supported_ids:
                ret.append(node_id)
                continue

            # Blocks with siblings can be removed
            all_blocks_have_other_supports = True
            for supported_ in supported_ids:
                supporting_blocks = self.depend_graph[supported_]
                if len(supporting_blocks) == 1:
                    all_blocks_have_other_supports = False
                    break
            if all_blocks_have_other_supports:
                ret.append(node_id)

        return ret

    def part1(self) -> str | int:
        """How many individual blocks could be removed, without affectin other blocks."""
        rem_ids = self.can_be_removed()
        return len(rem_ids)

    def _fall_count(self, id_: int):
        """Calculate how many other bricks would fall if this were removed."""
        block_is_supported = self.depend_graph.copy()
        count = 0
        would_fall = deque(list(self.support_graph[id_]))

        removed = {id_}
        removed_at_prev_try = {}
        while would_fall:
            try_next = would_fall.popleft()
            if try_next in removed:
                continue

            if len(block_is_supported[try_next] - removed) > 0:
                # Still supported...
                removed_now = hash(tuple(removed))
                if removed_at_prev_try.get(try_next, None) != removed_now:
                    # Try again after some another drops
                    would_fall.append(try_next)

                removed_at_prev_try[try_next] = removed_now
                continue

            # This block is falling
            removed.add(try_next)
            count += 1
            would_fall.extend(self.support_graph[try_next])

        return count

    def part2(self) -> str | int:
        """Sum of fall counts for each individual brick."""
        return sum(self._fall_count(id_) for id_ in self.brick_dic)
