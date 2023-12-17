import pytest

from advent_of_code.y23.day17 import ClumsyCrucible


@pytest.fixture
def sample_input() -> str:
    return """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


def test_part1(sample_input: str):
    assert ClumsyCrucible(sample_input).part1() == 102


@pytest.mark.skip
def test_part2(sample_input: str):
    assert ClumsyCrucible(sample_input).part2() == ...
