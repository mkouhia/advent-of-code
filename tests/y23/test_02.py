import pytest

from advent_of_code.y23.day02 import CubeConundrum, Game, CubeCombination


@pytest.fixture
def sample_games() -> str:
    return """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def test_reveal():
    spec = "3 blue, 4 red"
    expected = CubeCombination(blue=3, red=4)
    assert CubeCombination.from_string(spec) == expected


def test_game_from_record():
    record = "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    expected = Game(
        2,
        [
            CubeCombination(blue=1, green=2),
            CubeCombination(green=3, blue=4, red=1),
            CubeCombination(green=1, blue=1),
        ],
    )
    assert Game.from_record(record) == expected


@pytest.mark.parametrize("i", range(5))
def test_possible(i: int, sample_games: str):
    possible = [True, True, False, False, True]
    game_spec = sample_games.split("\n")[i]
    game = Game.from_record(game_spec)
    assert game.is_possible(red=12, green=13, blue=14) == possible[i]


def test_sample(sample_games):
    assert CubeConundrum(sample_games).part1() == 8


@pytest.mark.parametrize("i", [0, 1])
def test_minimum(i: int, sample_games: str):
    expected = [
        CubeCombination(red=4, green=2, blue=6),
        CubeCombination(red=1, green=3, blue=4),
    ]
    game_spec = sample_games.split("\n")[i]
    game = Game.from_record(game_spec)
    assert game.minimum_cubes() == expected[i]


@pytest.mark.parametrize("i", range(5))
def test_power(i: int, sample_games: str):
    game_spec = sample_games.split("\n")[i]
    game = Game.from_record(game_spec)
    expected = [48, 12, 1560, 630, 36]
    assert game.minimum_cubes().power() == expected[i]


def test_part2(sample_games: str):
    assert CubeConundrum(sample_games).part2() == 2286
