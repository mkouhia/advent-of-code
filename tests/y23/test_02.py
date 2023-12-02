import pytest

from advent_of_code.y23.day02 import CubeConundrum, Game, Reveal


def test_reveal():
    spec = "3 blue, 4 red"
    expected = Reveal(blue=3, red=4)
    assert Reveal.from_string(spec) == expected


def test_game_from_record():
    record = "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    expected = Game(
        2,
        [
            Reveal(blue=1, green=2),
            Reveal(green=3, blue=4, red=1),
            Reveal(green=1, blue=1),
        ],
    )
    assert Game.from_record(record) == expected


@pytest.mark.parametrize(
    "game_spec, possible",
    [
        ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
        ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
        (
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
            False,
        ),
        (
            "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
            False,
        ),
        ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True),
    ],
)
def test_possible(game_spec: str, possible: bool):
    game = Game.from_record(game_spec)
    assert game.is_possible(red=12, green=13, blue=14) == possible


def test_sample():
    input_text = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
    assert CubeConundrum.solve(input_text) == 8
