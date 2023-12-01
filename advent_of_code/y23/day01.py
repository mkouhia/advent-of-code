"""https://adventofcode.com/2023/day/1"""

_spelled_digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
_reverse_digits = {key[::-1]: val for key, val in _spelled_digits.items()}


def calibration_value(line: str) -> int:
    """Generate calibration value.

    On each line, the calibration value can be found by combining
    the first digit and the last digit (in that order) to form a single
    two-digit number.
    """
    return int(
        _first_digit(line, _spelled_digits) + _first_digit(line[::-1], _reverse_digits)
    )


def _first_digit(string_: str, spelled_digits) -> str:
    for i in range(len(string_)):
        char_ = string_[i]
        if char_ in "0123456789":
            return char_
        for key in spelled_digits:
            if string_[i : i + len(key)] == key:
                return spelled_digits[key]


def calibrate_document(document: str) -> int:
    """Return sum of calibration values for each row."""
    return sum(calibration_value(i) for i in document.splitlines())
