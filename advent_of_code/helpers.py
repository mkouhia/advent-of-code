"""Helper functions for Advent of Code."""

import re
from collections.abc import Iterable
from enum import Enum

import numpy as np


class TermColour(Enum):
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
