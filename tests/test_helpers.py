import numpy as np
from numpy.testing import assert_array_equal

import pytest

from advent_of_code.helpers import (
    TermColour,
    ResultCycler,
    char_array_to_string,
    highlight_by_pos,
    highlight_regex,
    to_numpy_array,
    partition_range,
)


class DemoCycler(ResultCycler):
    _expected = [1, 2, 3, 4, 5, 6, 7, 3, 4, 5, 6, 7, 3, 4]

    def __init__(self) -> None:
        self.i = 0
        self.result = 0

    def __hash__(self):
        return hash(self.result)

    def get_result(self):
        return self.result

    def run_cycle(self):
        self.i += 1
        self.result = self.i if self.i < 3 else (3 + (self.i - 3) % 5)


@pytest.mark.parametrize("i", list(range(1, 15)) + [47, 99])
def test_result_cycling(i):
    cycler = DemoCycler()
    expected = i if i < 3 else (3 + (i - 3) % 5)
    assert cycler.find_result_after(i) == expected


@pytest.mark.parametrize("i", list(range(1, 15)))  # + [47, 99])
def test_result_cumulative(i):
    cycler = DemoCycler()
    expected = [j if j < 3 else (3 + (j - 3) % 5) for j in range(1, i + 1)]
    print(expected, sum(expected))
    assert cycler.find_result_after(i, cumulative=True) == sum(expected)


def test_highlight_regex():
    res = highlight_regex(
        "a..#k", {"#": TermColour.OKGREEN, r"(\.)": TermColour.WARNING}
    )
    assert res == "a\x1b[93m.\x1b[0m\x1b[93m.\x1b[0m\x1b[92m#\x1b[0mk"


def test_highlight_by_pos():
    sample = """.....
.S-7.
.|.|.
.L-J.
....."""
    res = highlight_by_pos(
        sample, [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]
    )
    assert (
        res
        == ".....\n.\x1b[92mS\x1b[0m\x1b[92m-\x1b[0m\x1b[92m7\x1b[0m.\n.\x1b[92m|\x1b[0m.\x1b[92m|\x1b[0m.\n.\x1b[92mL\x1b[0m\x1b[92m-\x1b[0m\x1b[92mJ\x1b[0m.\n....."
    )


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
    arr = to_numpy_array(sample, "S")
    received = char_array_to_string(arr, encoding="ascii")
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
