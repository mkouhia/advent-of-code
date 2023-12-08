import pytest

from advent_of_code.y21.day06 import Lanternfish


@pytest.fixture
def sample_input() -> str:
    return "3,4,3,1,2"


def test_part1(sample_input: str):
    assert Lanternfish(sample_input).part1() == 5934


def test_part2(sample_input: str):
    assert Lanternfish(sample_input).part2() == 26984457539
