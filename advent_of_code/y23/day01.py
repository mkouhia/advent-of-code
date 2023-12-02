"""https://adventofcode.com/2023/day/1"""

from ..base import Puzzle


class Trebuchet(Puzzle):
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

    @classmethod
    def calibration_value(cls, line: str, use_spelled_digits=False) -> int:
        """Generate calibration value.

        Args:
            line: Input text, for which to generate calibration value.
            use_spelled_digits: Handle texts such as 'zero', 'one', ...,
              'nine' as digits.

        On each line, the calibration value can be found by combining
        the first digit and the last digit (in that order) to form a single
        two-digit number.
        """
        return int(
            cls._first_digit(line, cls._spelled_digits if use_spelled_digits else None)
            + cls._first_digit(
                line[::-1], cls._reverse_digits if use_spelled_digits else None
            )
        )

    def _first_digit(string_: str, spelled_digits) -> str:
        for i in range(len(string_)):
            char_ = string_[i]
            if char_ in "0123456789":
                return char_
            if spelled_digits is None:
                continue
            for key in spelled_digits:
                if string_[i : i + len(key)] == key:
                    return spelled_digits[key]

    @classmethod
    def part1(cls, document: str) -> int:
        """Return sum of calibration values for each row."""
        return sum(
            cls.calibration_value(i, use_spelled_digits=False)
            for i in document.splitlines()
        )

    @classmethod
    def part2(cls, document: str) -> int:
        """Return sum of calibration values for each row."""
        return sum(
            cls.calibration_value(i, use_spelled_digits=True)
            for i in document.splitlines()
        )
