"""https://adventofcode.com/2023/day/23"""

from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Iterable

import networkx as nx

from ..base import Puzzle


class LongWalk(Puzzle):

    """A Long Walk.

    Graph building and traversal problem. Find longest possible path.

    The graph is a directed acyclic graph.
    """

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        start_pos = (0, input_text.index("."))
        rows = input_text.strip().splitlines()
        self.end_pos = (len(rows) - 1, rows[-1].index("."))
        self.map = AsciiMap.from_string(input_text, start_pos)

    def part1(self) -> str | int:
        """Return longest walk that is possible.

        The graph was a directed acyclic graph, so there is a straight
        algorithm for this.
        """
        dg = nx.DiGraph()
        for elist in self.map.edges.values():
            e: Edge
            for e in elist:
                dg.add_edge(e.start_id, e.end_id, weight=e.weight)
        return nx.dag_longest_path_length(dg)

    def part2(self) -> str | int:
        """Whoops, the graph is not DAG anymore."""
        end_id = self.map.nodes[self.end_pos]
        weights = {}
        dg = nx.Graph()
        for elist in self.map.edges.values():
            e: Edge
            for e in elist:
                weights[(e.start_id, e.end_id)] = e.weight
                weights[(e.end_id, e.start_id)] = e.weight
                dg.add_edge(e.start_id, e.end_id, weight=e.weight)
        return longest_simple_paths(dg, 0, end_id, weights)


def longest_simple_paths(graph, source, target, weights) -> list[list]:
    """https://stackoverflow.com/a/64738743"""

    @cache
    def path_wt_(path):
        """Reduce constant counting together by caching a bit."""
        if len(path) == 2:
            return weights[path]
        half = len(path) // 2
        return path_wt_(tuple(path[: half + 1])) + path_wt_(tuple(path[half:]))

    longest_paths = []
    longest_path_length = 0
    for path in nx.all_simple_paths(graph, source=source, target=target):
        path_wt = path_wt_(tuple(path))
        if path_wt > longest_path_length:
            longest_path_length = path_wt
            longest_paths.clear()
            longest_paths.append(path)
        elif path_wt == longest_path_length:
            longest_paths.append(path)
    return longest_path_length


class Direction(Enum):
    N = (-1, 0)
    E = (0, 1)
    S = (1, 0)
    W = (0, -1)

    @classmethod
    def from_map(cls, char_):
        _map_chars = {c: d for c, d in zip("^>v<", "NESW")}
        return cls[_map_chars[char_]]

    def opposite(self):
        _opposite = {d: o for d, o in zip("NESW", "SWNE")}
        return Direction[_opposite[self.name]]

    @classmethod
    def all(cls):
        return [cls[d] for d in "NESW"]


@dataclass
class Edge:
    start_id: int
    end_id: int
    weight: int
    xy_locations: tuple[tuple[int, int], ...]


class AsciiMap:
    def __init__(
        self,
        map_text: str,
        nodes: dict[tuple[int, int], int],
        edges: dict[int, Edge],
    ) -> None:
        self.map_text = map_text
        self.nodes = nodes
        self.edges = edges

    def to_graphviz(self):
        edges = [
            f"  {e.start_id} -> {e.end_id};" for el in self.edges.values() for e in el
        ]
        return "digraph G {" + "\n".join(edges) + "}"

    @classmethod
    def from_string(cls, input_text: str, start_pos: tuple[int, int]):
        rows = input_text.strip().splitlines()
        shape = (len(rows), len(rows[0]))

        edges = {}
        nodes = {start_pos: 0}

        visited_xy = set([start_pos])
        node_q = deque([(start_pos, None)])
        while node_q:
            leg_start_n, dir_ = node_q.popleft()
            if dir_ is not None:
                dy, dx = dir_.value
                if (leg_start_n[0] + dy, leg_start_n[1] + dx) in visited_xy:
                    continue

            next_node, leg_xy, chars, pass_dirs = cls._process_leg(
                leg_start_n, dir_, visited_xy, rows, shape
            )
            if len(pass_dirs) == 0:
                # You shall not pass!
                continue

            if next_node not in nodes:
                nodes[next_node] = max(nodes.values()) + 1
                visited_xy.add(next_node)

            def _add_edge(i0, i1, locations):
                vert = Edge(i0, i1, len(locations) + 1, tuple(locations))
                if i0 not in edges:
                    edges[i0] = []
                edges[i0].append(vert)

            if 1 in pass_dirs:
                _add_edge(nodes[leg_start_n], nodes[next_node], leg_xy)
            if -1 in pass_dirs:
                _add_edge(nodes[next_node], nodes[leg_start_n], leg_xy[::-1])

            for next_, dir, _ in cls._next_positions(rows, shape, next_node):
                if next_ in visited_xy:
                    continue
                node_q.append((next_node, dir))

        return cls(input_text, nodes, edges)

    @classmethod
    def _process_leg(
        cls,
        start_node: tuple[int, int],
        start_dir: Direction,
        visited_xy: set[tuple[int, int]],
        rows,
        shape,
    ):
        """Goes until next crossing, creates connecting vertex and next node"""
        leg_xy = []
        chars = []
        next_ = start_node
        dir_ = start_dir
        pass_directions = [-1, 1]

        while True:
            if next_ == start_node:
                arg_ = {"moves": [start_dir]} if start_dir is not None else {}
            else:
                arg_ = {"exclude_moves": [dir_.opposite()]}

            next_opt = list(cls._next_positions(rows, shape, next_, **arg_))

            if len(next_opt) != 1:
                break

            if next_ != start_node:
                leg_xy.append(next_)
                chars.append(rows[next_[0]][next_[1]])

            next_, dir_, pass_dir = next_opt[0]
            if pass_dir != 0:
                reverse = -pass_dir
                if reverse in pass_directions:
                    pass_directions.remove(reverse)
            # if next_ in visited_xy:
            #     break

        visited_xy.update(leg_xy)

        return next_, leg_xy, chars, pass_directions

    @staticmethod
    def _next_positions(
        rows,
        shape,
        pos: tuple[int, int],
        moves: Iterable[Direction] = None,
        not_allowed=["#"],
        exclude_moves=None,
    ) -> Iterable[tuple[tuple[int, int], Direction, int]]:
        for move in moves or Direction.all():
            if exclude_moves and move in exclude_moves:
                continue
            new_y = pos[0] + move.value[0]
            new_x = pos[1] + move.value[1]

            if not ((0 <= new_y <= shape[0] - 1) and (0 <= new_x <= shape[1] - 1)):
                continue

            char_ = rows[new_y][new_x]
            if char_ in not_allowed:
                continue
            if char_ == ".":
                pass_direction = 0
            else:
                char_dir = Direction.from_map(char_)
                if char_dir is move:
                    pass_direction = 1
                else:
                    pass_direction = -1
                    assert char_dir is move.opposite()

            yield ((new_y, new_x), move, pass_direction)
