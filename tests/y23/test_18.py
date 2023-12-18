import pytest

from advent_of_code.y23.day18 import LavaductLagoon, Vertex, Direction


@pytest.fixture
def sample_input() -> str:
    return """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


@pytest.mark.parametrize(
    "hex_, dir, dist",
    [
        ("#70c710", "R", 461937),
        ("#0dc571", "D", 56407),
        ("#5713f0", "R", 356671),
        ("#d2c081", "D", 863240),
        ("#59c680", "R", 367720),
        ("#411b91", "D", 266681),
        ("#8ceee2", "L", 577262),
        ("#caa173", "U", 829975),
        ("#1b58a2", "L", 112010),
        ("#caa171", "D", 829975),
        ("#7807d2", "L", 491645),
        ("#a77fa3", "U", 686074),
        ("#015232", "L", 5411),
        ("#7a21e3", "U", 500254),
    ],
)
def test_convert_hex(hex_: str, dir: str, dist: int):
    v = Vertex.from_string_hex(f"X 0 ({hex_})")
    assert v == Vertex(Direction[dir], dist, hex_)


def test_part1(sample_input: str):
    lagoon = LavaductLagoon(sample_input)
    assert lagoon.part1() == 62


def test_part2(sample_input: str):
    assert LavaductLagoon(sample_input).part2() == 952408144115
