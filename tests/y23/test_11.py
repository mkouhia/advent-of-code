import pytest

from advent_of_code.y23.day11 import CosmicExpansion


@pytest.fixture
def sample_input() -> str:
    return """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


@pytest.fixture
def expanded() -> str:
    return """....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
"""


def test_init(sample_input):
    obj = CosmicExpansion(sample_input)
    assert obj.cosmos.galaxies == [
        (0, 3),
        (1, 7),
        (2, 0),
        (4, 6),
        (5, 1),
        (6, 9),
        (8, 7),
        (9, 0),
        (9, 4),
    ]


def test_expand(sample_input, expanded):
    original = CosmicExpansion(sample_input)
    new_cosmos = original.expand()

    assert new_cosmos.galaxies == CosmicExpansion(expanded).cosmos.galaxies


@pytest.mark.parametrize("factor, expected", [(2, 374), (10, 1030), (100, 8410)])
def test_expand_factor(sample_input, factor, expected):
    original = CosmicExpansion(sample_input)
    expanded = original.expand(factor)
    assert sum(expanded.distances()) == expected


def test_part1(sample_input: str):
    assert CosmicExpansion(sample_input).part1() == 374


def test_part2(sample_input: str):
    assert CosmicExpansion(sample_input).part2() == 82000210
