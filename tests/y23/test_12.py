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


def test_init():
    s = """#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1"""
    springs = HotSprings(s)
    print(springs.records)
    assert len(springs.records) == 6

@pytest.mark.parametrize('spec, count', [
    ('???.### 1,1,3', 1),
    ('.??..??...?##. 1,1,3', 4),
    ('?#?#?#?#?#?#?#? 1,3,1,6', 1 ),
    ('????.#...#... 4,1,1', 1 ),
    ('????.######..#####. 1,6,5', 4 ),
    ('?###???????? 3,2,1', 10),
])
def test_n_replacements(spec, count):
    record = ConditionRecord.from_string(spec)
    print(record)
    assert record.n_replacements() == count

# @pytest.mark.skip
def test_part1(sample_input: str):
    assert HotSprings(sample_input).part1() == 21


@pytest.mark.skip
def test_part2(sample_input: str):
    assert HotSprings(sample_input).part2() == ...
