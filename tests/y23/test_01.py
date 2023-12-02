import pytest
from advent_of_code.y23.day01 import Trebuchet


@pytest.mark.parametrize(
    "line, value",
    [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
    ],
)
def test_calibration_value(line: str, value: int):
    assert Trebuchet.calibration_value(line, use_spelled_digits=True) == value


def test_calibrate_document():
    test_content = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
    assert Trebuchet.part1(test_content) == 142
