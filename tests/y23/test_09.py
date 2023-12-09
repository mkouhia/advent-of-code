import numpy as np
import pytest

from numpy.testing import assert_array_equal

from advent_of_code.y23.day09 import MirageMaintenance


@pytest.fixture
def sample_input() -> str:
    return """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_init(sample_input: str):
    assert_array_equal(
        MirageMaintenance(sample_input).histories[1], np.array([1, 3, 6, 10, 15, 21])
    )


def test_part1(sample_input: str):
    assert MirageMaintenance(sample_input).part1() == 114


def test_part2(sample_input: str):
    assert MirageMaintenance(sample_input).part2() == 2
