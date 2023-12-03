import pytest

from advent_of_code.y23.day03 import GearRatios


@pytest.fixture
def sample_input() -> str:
    return """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


@pytest.fixture
def gear_ratios(sample_input) -> GearRatios:
    return GearRatios(sample_input)


def test_extract_numbers(gear_ratios):
    extracted = gear_ratios._extract_numbers()
    assert extracted.get((0, 0, 3)) == 467
    assert len(extracted) == 10


def test_part_numbers(gear_ratios):
    assert list(gear_ratios.part_numbers()) == [467, 35, 633, 617, 592, 755, 664, 598]


def test_part1(sample_input: str):
    assert GearRatios(sample_input).part1() == 4361


def test_part2(sample_input: str):
    assert GearRatios(sample_input).part2() == 467835
