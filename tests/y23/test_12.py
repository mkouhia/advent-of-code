import pytest

from advent_of_code.y23.day12 import ConditionRecord, HotSprings


@pytest.fixture
def sample_input() -> str:
    return """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


@pytest.mark.parametrize(
    "spec, count",
    [
        ("???#?. 3", 2),
        ("????. 1", 4),
        ("?#??. 1", 1),
        ("?##??. 1", 0),
        ("???.### 1,1,3", 1),
        (".??..??...?##. 1,1,3", 4),
        ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
        ("????.#...#... 4,1,1", 1),
        ("????.######..#####. 1,6,5", 4),
        ("?###???????? 3,2,1", 10),
        (".?###??????????### 3,2,1,3", 15),
        ("?###.????????.### 3,2,1,3", 15),
        ("?###.????????. 3,2,1", 15),
        ("..?###.????????. 3,2,1", 15),
        (".##.?#??.#.?# 2,1,1,1", 1),
        (".??????? 2,1", 10),
        (".????????. 2,1",  15),
        (".?###.###. 3,3", 1),
        (".??#??#??#??.#?.? 7,2", 1),
    ],
)
def test_n_replacements(spec, count):
    record = ConditionRecord.from_string(spec)
    assert record.n_replacements() == count

@pytest.mark.parametrize(
    "spec, count",
    [
        ("???.### 1,1,2", 0),
        ("???.### 1,1,3", 1),
        (".??..??...?##. 1,1,3", 16384),
        ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
        ("????.#...#... 4,1,1", 16),
        ("????.######..#####. 1,6,5", 2500),
        # ("?###???????? 3,2,1", 506250),
    ],
)
def test_n_replacements_part2(spec, count):
    record = ConditionRecord.from_string_part2(spec)
    print(record)
    assert record.n_replacements() == count


@pytest.mark.parametrize(
    "spec, expected",
    [
        (".# 1", ".#?.#?.#?.#?.# 1,1,1,1,1"),
        (
            "???.### 1,1,3",
            "???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3",
        ),
    ],
)
def test_expand_spec(spec, expected):
    assert ConditionRecord.expand_spec(spec) == expected


def test_part1(sample_input: str):
    assert HotSprings(sample_input).part1() == 21


def test_part2(sample_input: str):
    assert HotSprings(sample_input).part2() == 525152
