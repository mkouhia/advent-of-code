"""https://adventofcode.com/2021/day/19"""

import itertools
import math
import re
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property
from io import StringIO
from typing import Callable

import numpy as np
import open3d as o3d

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

        pattern = r'--- scanner (\d) ---\n((?:-?\d+,-?\d+,-?\d+\n)+)'
        for scanner_s in re.findall(pattern, input_text):
            id_ = int(scanner_s[0])
            beacons = np.genfromtxt(StringIO(scanner_s[1]), delimiter=',', dtype=int)
            self.scanners[id_] = Scanner(id_, beacons)
            
    def find_matches(self):
        """Start from 0. Traverse forward, find matches. Transform back."""
        ...

    def part1(self) -> str | int:
        return self.scanners[0].get_transforms(self.scanners[1])

    def part2(self) -> str | int:
        return super().part2()

@dataclass
class Scanner:
    id_: int
    beacons: np.ndarray

    def get_transforms(self, other: "Scanner", min_matches=12):
        """Match beacons by brute-force looping.
        
        Feature matching does not seem to work, since it seems there are
        so similar structures in the scopes.
        """
        current_beacons = {tuple(self.beacons[i].tolist()) for i in range(len(self.beacons))}
        other_len = len(other.beacons)
        for rotate_mat in rotations():
            candidates = (other.beacons @ rotate_mat).astype(int)
            for b0, i1 in itertools.product(self.beacons, range(other_len)):
                shift_vec = b0 - candidates[i1]
                other_tfm = candidates + shift_vec
                other_beacons = {tuple(other_tfm[i].tolist()) for i in range(other_len)}
                if len(common_beacons := current_beacons.intersection(other_beacons)) >= min_matches:
                    return rotate_mat, shift_vec, common_beacons
        raise UserWarning("No transform found")
                

    def translate_beacons(self, other: "Scanner", min_matches=12):
        """Translate beacons from other scanner to the same coordinates.

        Detect same beacons based on FPFH features. Translate coordinates
        of same beacons with least squares fit. Employ same transform to
        translate all other beacons.

        Args:
            min_matches: If less than N common matches, do not transform.

        Returns:
            None if not enough matches, otherwise translated coordinates.
        """
        transform = self._beacon_transform(other, min_matches)
        return transform(other.beacons)

    def _beacon_transform(self, other, min_matches):
        matches = self.get_transforms(other)
        # print(matches)
        if len(matches) < min_matches:
            return None

        source = other.beacons[list(matches.values())]
        target = self.beacons[list(matches.keys())]
        # print(source)
        # print(target)
        return least_squares_transform(source, target)


def cosine_similarity(vec, mat2) -> np.ndarray:
    """Calculate cosine similarity between each column combinations between mat1 and mat2."""
    p1 = vec.dot(mat2)
    p2 = np.linalg.norm(mat2, axis=0) * np.linalg.norm(vec)
    return p1/p2

def least_squares_transform(source: np.ndarray, target: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
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
        return np.dot(pad(x), A)[:,:-1]

    return translate