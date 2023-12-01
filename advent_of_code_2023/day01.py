"""https://adventofcode.com/2023/day/1"""


def calibration_value(line: str) -> int:
    """Generate calibration value.

    On each line, the calibration value can be found by combining
    the first digit and the last digit (in that order) to form a single
    two-digit number.
    """
    return int(_first_digit(line) + _first_digit(line[::-1]))


def _first_digit(string_: str) -> str:
    for char_ in string_:
        if char_ in "0123456789":
            return char_


def calibrate_document(document: str) -> int:
    """Return sum of calibration values for each row."""
    return sum(calibration_value(i) for i in document.splitlines())
