"""https://adventofcode.com/2021/day/19"""

import re
from dataclasses import dataclass
from functools import cached_property
from io import StringIO
from typing import Callable

import numpy as np
import open3d as o3d

from ..base import Puzzle

class BeaconScanner(Puzzle):

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.scanners = {}

        pattern = r'--- scanner (\d) ---\n((?:-?\d+,-?\d+,-?\d+\n)+)'
        for scanner_s in re.findall(pattern, input_text):
            id_ = int(scanner_s[0])
            beacons = np.genfromtxt(StringIO(scanner_s[1]), delimiter=',', dtype=int)
            self.scanners[id_] = Scanner(id_, beacons)


    def part1(self) -> str | int:
        return self.scanners[0].get_matches(self.scanners[1])

    def part2(self) -> str | int:
        return super().part2()

@dataclass
class Scanner:
    id_: int
    beacons: np.ndarray

    @cached_property
    def fpfh_features(self) -> np.ndarray:
        
        knn_normals=3
        knn_fpfh=5
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.beacons)

        pcd.estimate_normals(o3d.geometry.KDTreeSearchParamKNN(knn_normals))
        return o3d.pipelines.registration.compute_fpfh_feature(
            pcd,
            o3d.geometry.KDTreeSearchParamKNN(knn_fpfh)
        ).data


    def get_matches(self, other: "Scanner", threshold=0.9):
        """Match beacons based on cosine similarity of FPFH."""
        ret = {}
        n_beacons = len(self.beacons)
        for i in range(n_beacons):
            sim = cosine_similarity(self.fpfh_features[:, i], other.fpfh_features)
            
            j = sim.argmax()
            print(j, sim[j])
            if sim[j] >= threshold:
                ret[i] = j
        
        return ret
    
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
        matches = self.get_matches(other)
        if len(matches) < min_matches:
            return None
        
        source = other.beacons[list(matches.values())]
        target = self.beacons[list(matches.keys())]
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
        np.dot(pad(x), A)[:,:-1]

    return translate