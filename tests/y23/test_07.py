import pytest

from advent_of_code.y23.day07 import CamelCards, Hand


@pytest.fixture
def sample_input() -> str:
    return """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_sort(sample_input: str):
    cards = CamelCards(sample_input)
    assert cards.sorted_hands == [
        Hand("QQQJA", 483),
        Hand("T55J5", 684),
        Hand("KK677", 28),
        Hand("KTJJT", 220),
        Hand("32T3K", 765),
    ]


def test_part1(sample_input: str):
    assert CamelCards(sample_input).part1() == 6440


@pytest.mark.skip
def test_part2(sample_input: str):
    assert CamelCards(sample_input).part2() == ...
