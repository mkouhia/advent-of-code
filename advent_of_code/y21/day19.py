"""https://adventofcode.com/2021/day/19"""

from functools import cached_property
import itertools
import re
from collections.abc import Iterable
from dataclasses import dataclass
from io import StringIO
from typing import Callable

import numpy as np

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

    """Register mixed point measurements to one coordinate space."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.scanners: dict[int, Scanner] = {}

        pattern = r"--- scanner (\d+) ---\n((?:-?\d+,-?\d+,-?\d+\n)+)"
        for scanner_s in re.findall(pattern, input_text):
            id_ = int(scanner_s[0])
            beacons = np.genfromtxt(StringIO(scanner_s[1]), delimiter=",", dtype=int)
            self.scanners[id_] = Scanner(id_, beacons)

        self.rotations = {}
        self.centers = {}

    def find_matches(self):
        """Start from 0. Traverse forward, find matches. Transform back."""
        unmatched_scanners = self.scanners.copy()
        scanner_0 = unmatched_scanners.pop(0)
        global_scanner = Scanner(-1, scanner_0.beacons)
        matched_scanners = [0]

        def scan_distances(scanner_list=None):
            return iter(
                sorted(
                    [
                        (i1, len(global_scanner.common_distances(self.scanners[i1])))
                        for i1 in scanner_list
                    ],
                    key=lambda t: t[-1],
                    reverse=True,
                )
            )

        scanner_pairs = scan_distances([i for i in self.scanners if i != 0])
        min_matches = sum(1 for _ in itertools.combinations(range(12), 2))

        while len(unmatched_scanners) > 0:
            i1, n_matches = next(scanner_pairs)
            other = unmatched_scanners.pop(i1)
            if n_matches < min_matches:
                # Do reindexing
                unmatched_scanners[i1] = other  # Put back
                scanner_pairs = scan_distances(unmatched_scanners.keys())
                continue

            if i1 in matched_scanners:
                continue

            rotate_mat, shift_vec, _ = global_scanner.get_transforms(other)
            new_beacons = (other.beacons @ rotate_mat + shift_vec).astype(int)

            joined_beacons = np.unique(
                np.vstack([global_scanner.beacons, new_beacons]), axis=0
            )
            global_scanner = Scanner(-1, joined_beacons)

            matched_scanners.append(i1)
            self.rotations[i1] = rotate_mat
            self.centers[i1] = shift_vec

        return global_scanner.beacons

    def part1(self) -> str | int:
        return len(self.find_matches())

    def part2(self) -> str | int:
        self.find_matches()
        dists = [
            np.sum(np.abs(self.centers[i0] - self.centers[i1]))
            for i0, i1 in itertools.combinations(list(self.centers.keys()), 2)
        ]
        return max(dists)


@dataclass
class Scanner:

    """Registered points in one field of view."""

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
        # If shortest edge does not match, try looping

    return np.hstack((np.array([[node1], [node2]]), translation))


def match_nodes(
    dist1: np.ndarray, dist2: np.ndarray, node1: int, node2: int
) -> np.ndarray:
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
    common_distances, ind1, ind2 = np.intersect1d(
        dist1[node1], dist2[node2], return_indices=True
    )
    cond = common_distances > 0
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
