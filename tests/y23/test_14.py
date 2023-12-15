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


@pytest.fixture
def sample_packed() -> str:
    return """OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""


@pytest.mark.parametrize(
    "original, expected",
    [
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
    ],
)
def test_pack_string(original, expected):
    prd = ParabolicReflectorDish(original)
    print(prd.movable.dtype)
    assert False
    assert prd.pack_west().pattern == expected


@pytest.mark.parametrize(
    "original, expected",
    [
        ("O.....OO..", ".......OOO"),
        ("O.OO#....#", ".OOO#....#"),
        (".....##...", ".....##..."),
        ("OO.#O....O", ".OO#....OO"),
    ],
)
def test_pack_reverse(original, expected):
    prd = ParabolicReflectorDish(original)
    assert prd.pack_east().pattern == expected

def test_pattern(sample_input: str):
    prd = ParabolicReflectorDish(sample_input)
    assert prd.pattern == sample_input

def test_pack_north(sample_input: str, sample_packed: str):
    prd = ParabolicReflectorDish(sample_input)

    assert prd.pack_north().pattern == sample_packed

def test_pack_twice(sample_input: str, sample_packed: str):
    prd = ParabolicReflectorDish(sample_input)
    assert prd.pack_north().pack_north().pattern == sample_packed


@pytest.mark.parametrize(
    "cycles, expected",
    [
        (
            1,
            """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....""",
        ),
        (
            2,
            """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O""",
        ),
        (
            3,
            """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O""",
        ),
    ],
)
def test_pack_cycle(sample_input: str, cycles: int, expected: str):
    prd = ParabolicReflectorDish(sample_input)
    for _ in range(cycles):
        prd.pack_cycle()
    assert prd.pattern == expected


def test_part1(sample_input: str):
    assert ParabolicReflectorDish(sample_input).part1() == 136


def test_part2(sample_input: str):
    assert ParabolicReflectorDish(sample_input).part2() == 64
