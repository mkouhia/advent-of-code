import pytest

from advent_of_code.y23.day21 import StepCounter


@pytest.fixture
def sample_input() -> str:
    return """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def test_part1(sample_input: str):
    assert StepCounter(sample_input, n_steps=6).part1() == 16


@pytest.mark.skip
def test_part2(sample_input: str):
    assert StepCounter(sample_input).part2() == ...
