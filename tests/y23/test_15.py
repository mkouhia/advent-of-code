import pytest

from advent_of_code.y23.day15 import LensLibrary


@pytest.fixture
def sample_input() -> str:
    return "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_hash():
    assert LensLibrary.hash_("HASH") == 52


def test_part1(sample_input: str):
    assert LensLibrary(sample_input).part1() == 1320


def test_part2(sample_input: str):
    assert LensLibrary(sample_input).part2() == 145
