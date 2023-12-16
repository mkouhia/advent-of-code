import pytest

from advent_of_code.y23.day16 import TheFloorWillBeLava


@pytest.fixture
def sample_input() -> str:
    return r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


def test_part1(sample_input: str):
    assert TheFloorWillBeLava(sample_input).part1() == 46


def test_part2(sample_input: str):
    assert TheFloorWillBeLava(sample_input).part2() == 51
