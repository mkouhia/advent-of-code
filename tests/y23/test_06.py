import pytest

from advent_of_code.y23.day06 import WaitForIt, Race


@pytest.fixture
def sample_input() -> str:
    return """Time:      7  15   30
Distance:  9  40  200
"""


@pytest.mark.parametrize(
    "time, distance, expected_ways",
    [
        (7, 9, 4),
        (15, 40, 8),
        (30, 200, 9),
    ],
)
def test_race_ways(time: int, distance: int, expected_ways: int):
    assert Race(time, distance).ways_to_beat() == expected_ways


def test_part1(sample_input: str):
    assert WaitForIt(sample_input).part1() == 288


def test_part2(sample_input: str):
    assert WaitForIt(sample_input).part2() == 71503
