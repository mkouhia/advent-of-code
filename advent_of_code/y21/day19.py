"""https://adventofcode.com/2021/day/19"""

from functools import cached_property
import itertools
import re
from collections.abc import Iterable
from dataclasses import dataclass
from io import StringIO
from typing import Callable

import numpy as np
from tqdm import tqdm

from ..base import Puzzle


def rotations() -> Iterable[np.ndarray]:
    for x, y, z in itertools.permutations([0, 1, 2]):
        for sx, sy, sz in itertools.product([-1, 1], repeat=3):
            rotation_matrix = np.zeros((3, 3))
            rotation_matrix[0, x] = sx
            rotation_matrix[1, y] = sy
            rotation_matrix[2, z] = sz
            if np.linalg.det(rotation_matrix) == 1:
                yield rotation_matrix


def angles(a, b, c):
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.arccos(cosine_angle)


class BeaconScanner(Puzzle):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.scanners: dict[int, Scanner] = {}

        pattern = r"--- scanner (\d+) ---\n((?:-?\d+,-?\d+,-?\d+\n)+)"
        for scanner_s in re.findall(pattern, input_text):
            id_ = int(scanner_s[0])
            beacons = np.genfromtxt(StringIO(scanner_s[1]), delimiter=",", dtype=int)
            self.scanners[id_] = Scanner(id_, beacons)

    def find_matches(self):
        """Start from 0. Traverse forward, find matches. Transform back."""
        unmatched_scanners = self.scanners.copy()
        scanner_0 = unmatched_scanners.pop(0)

        global_scanner = Scanner(-1, scanner_0.beacons)

        ids = list(self.scanners.keys())
        scanner_common = [
            (i0, i1, len(self.scanners[i0].common_distances(self.scanners[i1])))
            for i0, i1 in itertools.combinations(ids, 2)
        ]

        matched_scanners = [-1, 0]
        false_combos = []

        min_matches = sum(1 for _ in itertools.combinations(range(12), 2))

        with tqdm(total=len(unmatched_scanners), desc="Matching  ") as pbar:
            while len(unmatched_scanners) > 0:
                test_order = sorted(
                    filter(
                        lambda t: (
                            t[0] in matched_scanners
                            and t[1] not in matched_scanners
                            and (t[0], t[1]) not in false_combos
                        ),
                        scanner_common,
                    ),
                    key=lambda t: t[-1],
                    reverse=True,
                )
                try:
                    test_next = next(iter(test_order))
                except StopIteration:
                    assert len(matched_scanners) == len(ids) + 1
                    break
                id_ = test_next[1]
                other = unmatched_scanners.pop(id_)

                if test_next[-1] < min_matches:
                    # Reindex matches
                    unmatched_scanners[id_] = other  # Put back
                    scanner_common = [
                        (
                            i0,
                            i1,
                            len(global_scanner.common_distances(self.scanners[i1])),
                        )
                        for i0, i1 in itertools.combinations(
                            [-1] + list(unmatched_scanners.keys()), 2
                        )
                    ]
                    continue
                try:
                    rotate_mat, shift_vec, _ = global_scanner.get_transforms(other)
                    new_beacons = (other.beacons @ rotate_mat + shift_vec).astype(int)

                    joined_beacons = np.unique(
                        np.vstack([global_scanner.beacons, new_beacons]), axis=0
                    )
                    global_scanner = Scanner(-1, joined_beacons)
                    pbar.update()
                    matched_scanners.append(id_)
                except UserWarning:
                    unmatched_scanners[id_] = other  # Put back
                    false_combos.append((test_next[0], test_next[1]))

        return global_scanner.beacons

    def part1(self) -> str | int:
        return len(self.find_matches())

    def part2(self) -> str | int:
        return super().part2()



@dataclass
class Scanner:
    id_: int
    beacons: np.ndarray

    def common_distances(self, other: "Scanner") -> np.ndarray:
        """Return distance values that are common with both scanners."""
        common = np.intersect1d(self.distances, other.distances)
        return common[common > 0]

    @cached_property
    def distances(self):
        """Returns distance (squared) matrix."""
        n_beacons = len(self.beacons)
        ret = np.empty((n_beacons, n_beacons), dtype=int)

        for i in range(n_beacons):
            ret[i, :] = np.power(self.beacons - self.beacons[i], 2).sum(axis=1)

        return ret

    def matching_beacons(self, other: "Scanner", min_matches=12):
        """Get indices of matching beacons.

        Args:
            other: Other beacon scanner.
            min_matches: Number of beacons that must match. Defaults to 12.
            
        Returns:
            Array (2 x N) containing matching beacon indices in scanners.
        """
        return common_subgraphs(self.distances, other.distances, min_matches)

    def get_transforms(self, other: "Scanner", min_matches=12):
        """Match beacons by brute-force looping.

        Go through all 24 possible rotations and all beacon combinations.

        Feature matching does not seem to work, since it seems there are
        so similar structures in the scopes.

        Args:
            min_matches: Amount of common beacons that need to be found
              for a transform to be accepted.

        Raises:
            UserWarning if no matching transform is found.

        Returns:
            - Rotation matrix: rotation that can be applied to other
              beacons as
            - Shift vector: vector that should be added to
            - Common beacons: Array (2 x N) containing matching beacon
              indices in scanners.


            Coordinate transforms should be applied to the other beacons
            as `(other.beacons @ rotate_mat + shift_vec).astype(int)` to
            get beacons in the coordinate space of the first beacon.

        """
        
        matches = self.matching_beacons(other, min_matches)
        i_this, i_other = matches[:, 0]
        # TODO compare this looping to matching with lstsq
        for rotate_mat in rotations():
            candidates = (other.beacons @ rotate_mat).astype(int)
            
            shift_vec = self.beacons[i_this] - candidates[i_other]
            other_tfm = candidates + shift_vec
            
            if np.array_equal(self.beacons[matches[0]], other_tfm[matches[1]]):
                # Rotation matches
                return rotate_mat, shift_vec, matches
        raise UserWarning("No transform found")


def common_subgraphs(dist1: np.ndarray, dist2: np.ndarray, min_matches: int):
    """Find common subgraphs in graphs, based on node distances.
    
    Start looking from the edge with smallest length.
    
    Args:
        dist1: Distance matrix between nodes in graph 1.
        dist2: Distance matrix between nodes in graph 2.
        min_matches: Amount of common edge lengths that need to be found
            for a subgraph to be accepted as common.

    Returns:
        Array (2 x N) containing matching node indices in graphs.
    """
    common_dist = np.intersect1d(dist1, dist2)
    
    # TODO if shortest edge does not match, start looping
    # Start from smallest distance (quite arbitrary)
    min_dist = np.min(common_dist[common_dist > 0])
    
    # Check both orientations for the first edge
    node1 = np.nonzero(dist1 == min_dist)[0][0]
    
    node2_opt = np.nonzero(dist2 == min_dist)[0]
    node2 = node2_opt[0]
    translation = match_nodes(dist1, dist2, node1, node2)
    if translation.shape == (2, 1):
        # It was the other direction
        node2 = node2_opt[1]
        translation = match_nodes(dist1, dist2, node1, node2)

    if translation.shape < (2, min_matches - 1):
        raise NotImplementedError(f"Subgraph does not have {min_matches} common nodes")
    
    return np.hstack((np.array([[node1], [node2]]), translation))

        
def match_nodes(dist1: np.ndarray, dist2: np.ndarray, node1: int, node2: int) -> np.ndarray:
    """Return common indices of nodes, based on distances.
    
    Assume that node1 and node2 are the same nodes in both graphs.

    Args:
        dist1: Distance matrix between nodes in graph 1.
        dist2: Distance matrix between nodes in graph 2.
        node1: Index of node in distance matrix 1.
        node2: Index of node in distance matrix 2.
        
    Returns:
        Array (2 x N) containing matching node indices in both graphs,
        matched by edge distances leaving nodes node1 and node2.
    """
    common_distances, ind1, ind2 = np.intersect1d(dist1[node1], dist2[node2], return_indices=True)
    cond = (common_distances > 0)
    return np.vstack((ind1[cond], ind2[cond]))


def cosine_similarity(vec, mat2) -> np.ndarray:
    """Calculate cosine similarity between each column combinations between mat1 and mat2."""
    p1 = vec.dot(mat2)
    p2 = np.linalg.norm(mat2, axis=0) * np.linalg.norm(vec)
    return p1 / p2


def least_squares_transform(
    source: np.ndarray, target: np.ndarray
) -> Callable[[np.ndarray], np.ndarray]:
    """Create transformation from one coordinate space to another.

    Args:
        source: points in source coordinates.
        target: points in target coordinates.

    Returns:
        Function, with which to transform any points in source coordinates
        into target coordinates.
    """

    def pad(x):
        return np.hstack([x, np.ones((x.shape[0], 1))])

    # Pad the data with ones, so that our transformation can do translations too
    X = pad(source)
    Y = pad(target)

    A, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)

    def translate(x):
        return np.dot(pad(x), A)[:, :-1]

    return translate
