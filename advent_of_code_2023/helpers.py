from pathlib import Path

import requests


def get_data(day: int, year=2023, session_id: str = None) -> str:
    """Get input data, either cached or downloaded."""
    cache_file = _get_cache_dir(day=day, year=year) / "input"
    if not cache_file.exists():
        text = _get_data_online(year=year, day=day, session_id=session_id)
        cache_file.write_text(text)
        return text

    return cache_file.read_text()


def _get_data_online(year, day, session_id) -> str:
    """Download input file from Advent of Code."""
    assert session_id is not None
    uri = "http://adventofcode.com/{year}/day/{day}/input".format(year=year, day=day)
    response = requests.get(uri, cookies={"session": session_id})
    return response.text


def _get_cache_dir(day, cache_root="~/.cache/advent_of_code_2023", year=2023) -> Path:
    loc = Path(cache_root).expanduser() / str(year) / str(day)

    if not loc.exists():
        loc.mkdir(parents=True)
    return loc
