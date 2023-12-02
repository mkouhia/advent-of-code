# Advent of Code solutions

This repository contains my solutions to [Advent of Code](https://adventofcode.com/) puzzles.

## Development

Upon a new puzzle:

- Create new file in `advent_of_code/y{year}/day{day}.py` for implementing solution. Derive puzzle solution class from `base::Puzzle`.
- Create test cases in `tests/y{year}/test_day{day}.py` for test driven development
- Run tests with `pytest tests/y{year}/test_day{day}.py`
- Add implemented classes in `advent_of_code/y{year}/__init__.py` dictionary `solutions`

### Running implemented solution against Advent of Code personal inputs

Run the developed method with `python -m advent_of_code run [--day DAY]`.

This will first download personal puzzle input file from the Advent of Code site and store it in local cache.
For downloading to work, get session ID from the Advent of Code cookie from your browser.
Save this text to file `.aoc_session_id`, and the program will read it from there.
