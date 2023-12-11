import numpy as np
from numpy.testing import assert_array_equal

import pytest

from advent_of_code.helpers import char_array_to_string, to_numpy_array, partition_range


def test_to_numpy_array():
    input = "ab \n12Y"
    expected = np.array(
        [
            ["a", "b", " "],
            ["1", "2", "Y"],
        ],
        dtype="U1",
    )
    assert_array_equal(to_numpy_array(input), expected)


def test_numpy_array_text():
    """See if text is same after numpy handling."""
    sample = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    arr = to_numpy_array(sample, 'S')
    received = char_array_to_string(arr, encoding='ascii')
    assert received == sample


@pytest.mark.parametrize(
    "source,partition_with,expected",
    [
        ((9, 15), (5, 12), (None, (9, 12), (12, 15))),
        ((5, 12), (9, 15), ((5, 9), (9, 12), None)),
        ((5, 15), (9, 12), ((5, 9), (9, 12), (12, 15))),
        ((5, 9), (12, 15), ((5, 9), None, None)),
        ((12, 15), (5, 9), (None, None, (12, 15))),
        ((5, 12), (12, 19), ((5, 12), None, None)),
    ],
)
def test_partition_range(
    source: tuple[int, int],
    partition_with: tuple[int, int],
    expected: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
):
    assert partition_range(source, partition_with) == expected
