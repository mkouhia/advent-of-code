import pytest

from advent_of_code.y23.day13 import Pattern, PointOfIncidence


@pytest.fixture
def sample_input() -> str:
    return """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

s = """.##.##.##....
#.######.##..
##......###..
...####......
...####...###
..#....#..#..
.#.####.#.###
..#....#..###
.##.##.##....
..######..###
#.##..##.####
#.#.##.#.....
##..##..##.##
.#..##..#....
#.##..##.##.."""

def test_part1(sample_input: str):
    assert PointOfIncidence(sample_input).part1() == 405

@pytest.mark.parametrize('pattern, col, row', [
    (""".##.##.##....
#.######.##..
##......###..
...####......
...####...###
..#....#..#..
.#.####.#.###
..#....#..###
.##.##.##....
..######..###
#.##..##.####
#.#.##.#.....
##..##..##.##
.#..##..#....
#.##..##.##..""", 12, 0)
])
def test_samples(pattern, col, row):
    p = Pattern(pattern)
    assert p.mirror_col() == col
    assert p.mirror_row() == row

@pytest.mark.skip
def test_part2(sample_input: str):
    assert PointOfIncidence(sample_input).part2() == ...
