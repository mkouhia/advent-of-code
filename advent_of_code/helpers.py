"""Helper functions for Advent of Code."""

import itertools
import re
from collections.abc import Iterable
from enum import Enum
from typing import Callable

import numpy as np


class TermColour(Enum):

    """Colours for printing in the terminal."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def highlight_regex(text: str, pattern_dic: dict[str, TermColour]):
    """Highlight inputs by regex pattern"""
    out = text
    for key, col in pattern_dic.items():
        repl = r"\1" if key.startswith("(") and key.endswith(")") else key
        out = re.sub(key, f"{col.value}{repl}{TermColour.ENDC.value}", out)
    return out


def highlight_by_pos(
    text: str, coords: Iterable[int, int], color: TermColour = TermColour.OKGREEN
):
    """Highlight text by coordinates in the original string."""
    ret = ""
    coords_order = sorted(coords)
    for i, row in enumerate(text.splitlines()):
        for j, char_ in enumerate(row):
            if len(coords_order) == 0:
                ret += row[j:]
                break
            if len(coords_order) > 0 and (i, j) == coords_order[0]:
                coords_order.pop(0)
                char_ = f"{color.value}{char_}{TermColour.ENDC.value}"
            ret += char_
        ret += "\n"
    if not text.endswith("\n"):
        return ret[:-1]
    return ret


def to_numpy_array(data: str, dtype="U") -> np.ndarray:
    """Read fixed-width text string to Numpy array.

    Args:
        dtype: Numpy short data type, 'S' or 'U'
    """
    nparr = np.array(data.split("\n"), dtype=dtype)
    return nparr.view(f"{dtype}1").reshape((nparr.size, -1))


def char_array_to_string(arr: np.ndarray, encoding="utf-8") -> str:
    """Convert char array back to string."""
    col = np.full((arr.shape[0], 1), "\n", dtype=arr.dtype)
    return np.hstack((arr, col)).tobytes().decode(encoding).replace("\x00", "").strip()


def area_by_vertices(vertices: Iterable[int, int], boundary: int) -> float:
    """Calculate polygon area with integer vertex coordinates.

    Area within the area enclosed by vertices are calculated by the
    Shoelace formula. In the Advent of Code puzzles, typically the vertices
    are organized in an orthogonal grid, with boundary thickness=1; this
    boundary is often included or excluded.

    Args:
        vertices: Iterable of (x, y) or (y, x) points.
        boundary: Handling of the boundary. If `boundary==0`, return the
          area from Shoelace formula directly. If `boundary==-1`, return
          the area inside the boundary, not including the boundary itself.
          If `boundary==1`, include the boundary thickness.

    Returns:
        Area, in vertex units.

    https://en.wikipedia.org/wiki/Shoelace_formula
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    pts = vertices
    if vertices[-1] != vertices[0]:
        pts.append(vertices[0])
    area = 0
    p_len = 0
    for p0, p1 in itertools.pairwise(vertices):
        area += (p0[0] + p1[0]) * (p0[1] - p1[1])
        p_len += abs(p1[0] - p0[0]) + abs(p1[1] - p0[1])

    area = abs(int(area * 0.5))

    if not boundary:
        return area
    if boundary < 0:
        return area - (p_len // 2) + 1
    return area + (p_len // 2) + 1


def point_angles(a, b, c):
    """Calculate angle by points abc, where b is center point."""
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.arccos(cosine_angle)


def cosine_similarity(vec: np.ndarray, mat2: np.ndarray) -> np.ndarray:
    """Cosine similarity between vector and each column in mat1."""
    p1 = vec.dot(mat2)
    p2 = np.linalg.norm(mat2, axis=0) * np.linalg.norm(vec)
    return p1 / p2


def least_squares_transform(
    source: np.ndarray,
    target: np.ndarray,
    shift=True,
) -> Callable[[np.ndarray], np.ndarray]:
    """Create transformation from one coordinate space to another.

    Args:
        source: points in source coordinates.
        target: points in target coordinates.
        shift: Allow translation? Default: True.

    Returns:
        Function, with which to transform any points in source coordinates
        into target coordinates.
    """

    def pad(x):
        """Add vector column of ones to the end."""
        return np.hstack([x, np.ones((x.shape[0], 1))])

    if shift:
        # Add vector at the end, so also translations are possible
        source = pad(source)
        target = pad(target)

    sol, _, _, _ = np.linalg.lstsq(source, target, rcond=None)

    def translate(mat):
        if shift:
            return np.dot(pad(mat), sol)[:, :-1]
        return np.dot(mat, sol)

    return translate


def partition_range(
    source: tuple[int, int], partition_with: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Partition source range with another range.

    Example:
                    5       9     12    15
    source                  [------------)
    partition_with  [--------------)

        partition_range(source=(9,15), partition_with=(5,12))
        >>> (None, (9, 12), (12, 15))

    Args:
        source: Range to be partitioned, (start, end).
        partition_with: Range, with which to partition the first.

    Returns:
        Three ranges related to the original: before, overlap, after. If some
        range is not present (e.g. partitioning does not result in range before
        partitionining range), the particular tuple will be None.
    """
    if source[1] < partition_with[0]:
        return source, None, None

    if partition_with[1] < source[0]:
        return None, None, source

    before = (source[0], partition_with[0]) if source[0] < partition_with[0] else None

    after = (partition_with[1], source[1]) if partition_with[1] < source[1] else None

    overlap_pts = (max(source[0], partition_with[0]), min(source[1], partition_with[1]))
    overlap = overlap_pts if (overlap_pts[0] < overlap_pts[1]) else None

    return before, overlap, after


class ExtRange:

    """Extended range."""

    def __init__(self, *subranges):
        self.subranges = []
        for sub in subranges:
            if isinstance(sub, range):
                self.subranges.append(sub)
            else:
                self.subranges.append(range(*sub))

    def __repr__(self) -> str:
        return f'<Range({",".join(map(str, self.subranges))})>'

    def simple_repr(self) -> str:
        """Simple representation of ranges.

        Ranges are converted to first:last, where both are inclusive. Single
        element ranges are shown as one element.

        Example:
            >>> k = [-5, -4, 0, 1, 2, 4, 7, 8, 9, 11]
            >>> ExtRange.from_int_list(k).simple_repr()
            '-5:-4,0:2,4,7:9,11'
        """

        def str_sub(s: range):
            return str(s.start) if s.start == s.stop - 1 else f"{s.start}:{s.stop-1}"

        return ",".join(str_sub(s) for s in self.subranges)

    @classmethod
    def from_int_list(cls, int_list: list[int]) -> "ExtRange":
        return cls(*cls.int_list_to_range_limits(int_list))

    @staticmethod
    def int_list_to_range_limits(int_list: list[int]) -> Iterable[tuple[int, int]]:
        """Convert list of integers into [start, end) endpoints used in ranges.

        Expect that input list is ordered.

        Yields:
            Tuples [start, end) for each subrange in input list.
        """
        for _, b in itertools.groupby(
            enumerate(int_list), lambda pair: pair[1] - pair[0]
        ):
            b = list(b)
            yield b[0][1], b[-1][1] + 1
