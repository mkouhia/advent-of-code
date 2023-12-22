import pytest

from advent_of_code.y23.day22 import Brick, SandSlabs


@pytest.fixture
def sample_input() -> str:
    return """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


def test_brick_from_spec():
    assert Brick.from_spec("1,0,1~1,2,1") == Brick((1, 1), (0, 2), (1, 1))


def test_part1(sample_input: str):
    assert SandSlabs(sample_input).part1() == 5


def test_part2(sample_input: str):
    assert SandSlabs(sample_input).part2() == 7
