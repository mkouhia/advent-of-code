import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from advent_of_code.y23.day24 import NeverTellMeTheOdds, Vector


@pytest.fixture
def sample_input() -> str:
    return """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


@pytest.mark.parametrize(
    "s1,s2,expected",
    [
        ("19, 13, 30 @ -2, 1, -2", "18, 19, 22 @ -1, -1, -2", (14.333, 15.333)),
        ("19, 13, 30 @ -2, 1, -2", "20, 25, 34 @ -2, -2, -4", (11.667, 16.667)),
        ("19, 13, 30 @ -2, 1, -2", "12, 31, 28 @ -1, -2, -1", (6.2, 19.4)),
        ("19, 13, 30 @ -2, 1, -2", "20, 19, 15 @ 1, -5, -3", -1),
        ("18, 19, 22 @ -1, -1, -2", "20, 25, 34 @ -2, -2, -4", 0),
        ("18, 19, 22 @ -1, -1, -2", "12, 31, 28 @ -1, -2, -1", (-6, -5)),
        ("18, 19, 22 @ -1, -1, -2", "20, 19, 15 @ 1, -5, -3", -1),
        ("20, 25, 34 @ -2, -2, -4", "12, 31, 28 @ -1, -2, -1", (-2, 3)),
        ("20, 25, 34 @ -2, -2, -4", "20, 19, 15 @ 1, -5, -3", -1),
        ("12, 31, 28 @ -1, -2, -1", "20, 19, 15 @ 1, -5, -3", -1),
    ],
)
def test_intersect(s1, s2, expected):
    v1 = Vector.from_string(s1)
    v2 = Vector.from_string(s2)

    result = v1.paths_intersect_xy(v2)
    if isinstance(expected, int):
        assert result == expected
    else:
        assert_array_almost_equal(result, expected, decimal=3)


def test_intersections(sample_input: str):
    part1 = NeverTellMeTheOdds(sample_input)
    assert part1.num_intersections((7, 27)) == 2


def test_part2(sample_input: str):
    assert NeverTellMeTheOdds(sample_input).part2() == 47
