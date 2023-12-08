import pytest

from advent_of_code.y23.day08 import HauntedWasteland


@pytest.mark.parametrize(
    "input_text, steps",
    [
        (
            """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""",
            2,
        ),
        (
            """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""",
            6,
        ),
    ],
)
def test_part1(input_text: str, steps: int):
    assert HauntedWasteland(input_text).part1() == steps


def test_part2():
    input_text = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
    assert HauntedWasteland(input_text).part2() == 6
