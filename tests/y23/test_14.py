import pytest

from advent_of_code.y23.day14 import ParabolicReflectorDish


@pytest.fixture
def sample_input() -> str:
    return """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


@pytest.mark.parametrize("original, expected", [
    ("O....#....", "O....#...."),
    ("O.OO#....#", "OOO.#....#"),
    (".....##...", ".....##..."),
    ("OO.#O....O", "OO.#OO...."),
    (".O.....O#.", "OO......#."),
    ("O.#..O.#.#", "O.#O...#.#"),
    ("..O..#O..O", "O....#OO.."),
    (".......O..", "O........."),
    ("#....###..", "#....###.."),
    ("#OO..#....", "#OO..#...."),
])
def test_pack_string(original, expected):
    assert ParabolicReflectorDish.pack_string(original) == expected

def test_pack_north(sample_input: str):
    prd = ParabolicReflectorDish(sample_input)
    expected = """OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""
    assert prd.pack_north().pattern == expected
    
def test_part1(sample_input: str):
    assert ParabolicReflectorDish(sample_input).part1() == 136


@pytest.mark.skip
def test_part2(sample_input: str):
    assert ParabolicReflectorDish(sample_input).part2() == ...
