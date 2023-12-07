"""https://adventofcode.com/2023/day/7"""

import collections
from ..base import Puzzle


class Hand:

    """A hand in game of Camel Cards."""

    _types = [
        (1, 1, 1, 1, 1),  # High pair
        (2, 1, 1, 1),  # One pair
        (2, 2, 1),  # Two pairs
        (3, 1, 1),  # Three of a kind
        (3, 2),  # Full house
        (4, 1),  # Four of a kind
        (5,),  # Five of a kind
    ]
    _card_order = "23456789TJQKA"

    def __init__(self, cards: str, bid: int) -> None:
        self.cards = cards
        self.bid = bid

    @property
    def strength(self) -> tuple[int, int, int, int, int, int]:
        """Strength of a hand. Greater is better."""
        vals = sorted(collections.Counter(self.cards).values(), reverse=True)
        type_s = self._types.index(tuple(vals))

        card_s = [self._card_order.index(j) for j in self.cards]

        return tuple([type_s] + card_s)

    def __lt__(self, other: "Hand"):
        return self.strength < other.strength

    def __eq__(self, other: "Hand"):
        return self.cards == other.cards


class CamelCards(Puzzle):

    """A game of camel cards."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.hands = [
            Hand(parts[0], int(parts[1]))
            for i in input_text.strip().splitlines()
            if len(parts := i.split(" ")) > 0
        ]

    def part1(self) -> str | int:
        """Returns total winnings; sum of ranks multiplied by bids."""
        sorted_hands = sorted(self.hands, reverse=True)
        points = list(range(len(sorted_hands), 0, -1))
        pts = [i[0].bid * i[1] for i in zip(sorted_hands, points)]
        return sum(pts)

    def part2(self) -> str | int:
        return
