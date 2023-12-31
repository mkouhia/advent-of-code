"""https://adventofcode.com/2023/day/25"""

from collections import Counter
import random

from ..base import Puzzle


class Snowverload(Puzzle):
    def build_graph(self) -> tuple[list[str], list[tuple[int, int]]]:
        edges = []
        nodes = []

        def get_idx(node):
            if node not in nodes:
                nodes.append(node)
                return len(nodes) - 1
            else:
                return nodes.index(node)

        for line in self.input_text.strip().splitlines():
            from_, to_arr = line.split(":")
            i = get_idx(from_)

            for to_ in to_arr.strip().split(" "):
                j = get_idx(to_)
                edges.append((i, j))

        return nodes, edges

    def part1(self) -> str | int:
        random.seed(0)
        nodes, edges = self.build_graph()
        graph = DisjointSet.of(len(nodes))

        n_cut = 0
        while n_cut != 3:
            g = graph.copy()
            g, edges_remain = self.contract(g, edges)

            n_cut = 0
            roots = set()
            for i in edges_remain:
                u, v = edges[i]
                ur, vr = [g.find(j) for j in (u, v)]
                if ur != vr:
                    roots.update((ur, vr))
                    n_cut += 1
            print(roots, n_cut)

        counts = Counter()
        for i in range(len(nodes)):
            counts.update((g.find(i),))

        vals = list(counts.values())
        print(counts)
        assert len(vals) == 2

        return vals[0] * vals[1]

    def part2(self) -> str | int:
        return super().part2()

    @staticmethod
    def contract(graph: "DisjointSet", edges, t=2):
        n_edges = len(edges)
        n_verts = len(graph.forest)
        order_ = random.sample(range(n_edges), n_edges)
        i = 0
        while n_verts > t:
            from_, to_ = edges[order_[i]]
            if graph.union(from_, to_):
                n_verts -= 1
            i += 1

        return graph, order_[i:]


class Set:
    def __init__(self, parent: int, rank: int):
        self.parent = parent
        self.rank = rank

    def __repr__(self):
        return f"<Set({self.parent}, {self.rank})>"

    def copy(self):
        return Set(self.parent, self.rank)


class DisjointSet:

    """Disjoint-set data structure.

    https://en.wikipedia.org/wiki/Disjoint-set_data_structure
    """

    def __init__(self, forest: list[Set]) -> None:
        self.forest = forest

    @classmethod
    def of(cls, n_verts: int):
        forest = [Set(parent=i, rank=0) for i in range(n_verts)]
        return cls(forest)

    def copy(self):
        return DisjointSet([s.copy() for s in self.forest])

    def find(self, x: int) -> int:
        """Find root element, with path compression"""
        if self.forest[x].parent != x:
            self.forest[x].parent = self.find(self.forest[x].parent)
            return self.forest[x].parent
        return x

    def union(self, x: int, y: int):
        """Merge trees with roots x and y."""
        # Replace nodes by roots
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return  # x and y are already in the same set

        # If necessary, rename variables to ensure that
        # x has rank at least as large as that of y
        if self.forest[x].rank < self.forest[y].rank:
            (x, y) = y, x

        # Make x the new root
        self.forest[y].parent = x
        # If necessary, increment the rank of x
        if self.forest[x].rank == self.forest[y].rank:
            self.forest[x].rank += 1

        return True
