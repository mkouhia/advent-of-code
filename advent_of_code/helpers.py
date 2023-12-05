"""Helper functions for Advent of Code."""

from pathlib import Path

import requests
import numpy as np


def to_numpy_array(data: str) -> np.ndarray:
    """Read fixed-width text string to Numpy array."""
    nparr = np.array(data.split("\n"), dtype="str")
    return nparr.view("U1").reshape((nparr.size, -1))


def partition_range(
    source: tuple[int, int], partition_with: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Partition source range with another range.

    Example:
                    5       9     12    15
    source                  [------------)
    partition_with  [--------------)

        partition_range(source=(9,15), partition_with=(5,12))
        >>> (None, (9, 12), (12, 15))

    Args:
        source: Range to be partitioned, (start, end).
        partition_with: Range, with which to partition the first.

    Returns:
        Three ranges related to the original: before, overlap, after. If some
        range is not present (e.g. partitioning does not result in range before
        partitionining range), the particular tuple will be None.
    """
    if source[1] < partition_with[0]:
        return source, None, None

    if partition_with[1] < source[0]:
        return None, None, source

    before = (source[0], partition_with[0]) if source[0] < partition_with[0] else None

    after = (partition_with[1], source[1]) if partition_with[1] < source[1] else None

    overlap_pts = (max(source[0], partition_with[0]), min(source[1], partition_with[1]))
    overlap = overlap_pts if (overlap_pts[0] < overlap_pts[1]) else None

    return before, overlap, after


def get_data(year: int, day: int) -> str:
    """Get input data, either cached or downloaded.

    First try to get cached data. If that does not exist, try to
    download the input file from Advent of Code. Downloading requires
    session ID cookie information.

    Raises:
        UserWarning if trying to download and session ID is not found.
    """
    cache_file = _get_cache_dir(day=day, year=year) / "input"
    if not cache_file.exists():
        text = _get_data_online(year=year, day=day)
        cache_file.write_text(text, encoding="utf-8")
        return text

    return cache_file.read_text(encoding="utf-8")


def _get_data_online(year: int, day: int) -> str:
    """Download input file from Advent of Code."""
    session_id = _get_session_id()
    uri = f"http://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(uri, cookies={"session": session_id}, timeout=5)
    return response.text


def _get_cache_dir(year: int, day: int, cache_root="~/.cache/advent_of_code") -> Path:
    loc = Path(cache_root).expanduser() / str(year) / str(day)

    if not loc.exists():
        loc.mkdir(parents=True)
    return loc


def _get_session_id() -> str:
    """Try to read session ID cookie from disk.

    Raises:
        UserWarning if file .aoc_session_id is not found.
    """
    dotfile = Path(".aoc_session_id")
    if not dotfile.exists():
        raise UserWarning("Session ID not found in file .aoc_session_id")

    return dotfile.read_text(encoding="utf-8").strip("\n")


def create_new_template(year: int, day: int) -> tuple[Path, Path]:
    """Create new development and test files for a puzzle.

    Returns:
        Paths to created development and test files.
    """
    year_str = f"y{year - 2000}"
    module_str = f"day{day:02}"
    class_name = f"Solution{year_str.capitalize()}{module_str.capitalize()}"

    content = {
        "dev": f'''"""https://adventofcode.com/{year}/day/{day}"""

from ..base import Puzzle

class {class_name}(Puzzle):
    
    def part1(self) -> str | int:
        return super().part1()
    
    def part2(self) -> str | int:
        return super().part2()
''',
        "test": f"""import pytest

from advent_of_code.{year_str}.{module_str} import {class_name}


@pytest.fixture
def sample_input() -> str:
    return ...


@pytest.mark.skip
def test_part1(sample_input: str):
    assert {class_name}(sample_input).part1() == ...


@pytest.mark.skip
def test_part2(sample_input: str):
    assert {class_name}(sample_input).part2() == ...
""",
    }
    locations = {
        "dev": Path("advent_of_code", year_str, f"{module_str}.py"),
        "test": Path("tests", year_str, f"test_{day:02}.py"),
    }

    for key, location in locations.items():
        if not location.exists():
            location.parent.mkdir(exist_ok=True, parents=True)
            location.write_text(content[key], encoding="utf-8")

    return tuple(locations.values())
