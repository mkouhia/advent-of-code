import pytest

from advent_of_code.y23.day21 import StepCounter


@pytest.fixture
def sample_input() -> str:
    return """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def test_part1(sample_input: str):
    sc = StepCounter(sample_input)
    assert sc.n_loc(sc.start_pos, 6) == 16


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, {"a_odd": 1, "a_even": 0, "b_": 1, "c_": 0, "d_": 1}),
        (2, {"a_odd": 4, "a_even": 1, "b_": 1, "c_": 1, "d_": 2}),
        (3, {"a_odd": 9, "a_even": 4, "b_": 1, "c_": 2, "d_": 3}),
        (4, {"a_odd": 16, "a_even": 9, "b_": 1, "c_": 3, "d_": 4}),
    ],
)
def test_pos(n, expected):
    assert StepCounter.after_n(n) == expected


@pytest.mark.parametrize("n,expected", [(4, 25), (7, 64), (26501365, 702322399865956)])
def test_part2(n, expected):
    s = "...\n.S.\n..."
    assert StepCounter(s).locs_after(n) == expected


@pytest.fixture
def reddit_sample():
    return """.................
..#..............
...##........###.
.............##..
..#....#.#.......
.......#.........
......##.##......
...##.#.....#....
........S........
....#....###.#...
......#..#.#.....
.....#.#..#......
.#...............
.#.....#.#....#..
...#.........#.#.
...........#..#..
................."""


@pytest.fixture
def sample_odd():
    """Same as Reddit sample, but 2 rows/cols less -> d/2=7"""
    return """...............
..#............
...##......###.
...........##..
..#............
...............
......#.#......
.......S.......
......#..#.....
.....#..#......
.#.............
.#..........#..
...#.......#.#.
.........#..#..
..............."""


@pytest.fixture
def sample_stacked(reddit_sample):
    return stack_s(reddit_sample, 9)


@pytest.fixture
def sample_odd_stacked(sample_odd):
    return stack_s(sample_odd, 9)


@pytest.mark.parametrize(
    "n,expected",
    [
        # (7, 52),
        # (8, 68),
        (25, 576),
        (42, 1576),
        (59, 3068),
        (76, 5052),
        (1180148, 1185525742508),
    ],
)
def test_part2(n, expected, reddit_sample):
    assert StepCounter(reddit_sample).locs_after(n) == expected


@pytest.mark.parametrize(
    "n,expected",
    [
        (25, 576),
        (42, 1576),
        (59, 3068),
        (76, 5052),
    ],
)
def test_expanded(n, expected, sample_stacked):
    sc = StepCounter(sample_stacked)
    count_stacked = sc.n_loc(sc.start_pos, n)
    assert count_stacked == expected


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_odd(n, sample_odd, sample_odd_stacked):
    k = len(sample_odd.splitlines())
    steps = n * k + k // 2
    part2 = StepCounter(sample_odd).locs_after(steps)
    sc = StepCounter(sample_odd_stacked)
    count_stacked = sc.n_loc(sc.start_pos, steps)
    assert count_stacked == part2


def stack_s(s: str, n: int) -> str:
    lines = s.replace("S", ".").strip().splitlines()
    lines_w = list(map("".join, zip(*([lines] * n))))
    lines_x = lines_w * n
    pos = len(lines_x) // 2

    midline = list(lines_x[pos])
    midline[pos] = "S"
    lines_x[pos] = "".join(midline)
    return "\n".join(lines_x)
