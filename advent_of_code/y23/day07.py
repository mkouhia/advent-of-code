"""https://adventofcode.com/2023/day/7"""

import collections
from ..base import Puzzle


Hand = collections.namedtuple("Hand", ["cards", "bid"])


class CamelCards(Puzzle):

    """A game of camel cards."""

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

    def __init__(self, input_text: str, joker_rule=False) -> None:
        super().__init__(input_text)
        self.joker_rule = joker_rule
        self.hands = [
            Hand(parts[0], int(parts[1]))
            for i in input_text.strip().splitlines()
            if len(parts := i.split(" ")) > 0
        ]

    @property
    def sorted_hands(self):
        return sorted(self.hands, key=lambda hand: self.strength(hand), reverse=True)

    def strength(self, hand: Hand) -> tuple[int, int, int, int, int, int]:
        """Strength of a hand. Greater is better."""
        vals = sorted(collections.Counter(hand.cards).values(), reverse=True)
        type_s = self._types.index(tuple(vals))

        card_s = [self._card_order.index(j) for j in hand.cards]

        return tuple([type_s] + card_s)

    def part1(self) -> str | int:
        """Returns total winnings; sum of ranks multiplied by bids."""
        points = list(range(len(self.hands), 0, -1))
        pts = [i[0].bid * i[1] for i in zip(self.sorted_hands, points)]
        return sum(pts)

    def part2(self) -> str | int:
        return
