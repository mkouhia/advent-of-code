"""https://adventofcode.com/2023/day/7"""

import collections
from ..base import Puzzle


Hand = collections.namedtuple("Hand", ["cards", "bid"])


class CamelCards(Puzzle):

    """A game of camel cards."""

    _types = [
        (1, 1, 1, 1, 1),  # High card
        (2, 1, 1, 1),  # One pair
        (2, 2, 1),  # Two pairs
        (3, 1, 1),  # Three of a kind
        (3, 2),  # Full house
        (4, 1),  # Four of a kind
        (5,),  # Five of a kind
    ]
    _card_order = None
    _card_order_rules = {
        "std": "23456789TJQKA",
        "joker": "J23456789TQKA",
    }

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.set_joker_rule(False)
        self.hands = [
            Hand(parts[0], int(parts[1]))
            for i in input_text.strip().splitlines()
            if len(parts := i.split(" ")) > 0
        ]

    def set_joker_rule(self, mode: bool = True):
        """Set joker rule to take effect."""
        self.joker_rule = mode
        self._card_order = self._card_order_rules["joker" if mode else "std"]

    @property
    def sorted_hands(self):
        """Get hands, in sorted order."""
        return sorted(self.hands, key=self.strength, reverse=True)

    def strength(self, hand: Hand) -> tuple[int, int, int, int, int, int]:
        """Strength of a hand. Greater is better."""

        if self.joker_rule and "J" in hand.cards:
            # Replace J with most beneficial
            counted = collections.Counter(i for i in hand.cards)
            joker_count = counted.pop("J") if "J" in counted else 0
            if joker_count == 5:
                vals = [5]
            else:
                vals = sorted(counted.values(), reverse=True)
                vals[0] += joker_count
                while sum(vals) < 5:
                    vals.append(1)

        else:
            vals = sorted(collections.Counter(hand.cards).values(), reverse=True)

        type_s = self._types.index(tuple(vals))

        card_s = [self._card_order.index(j) for j in hand.cards]

        return tuple([type_s] + card_s)

    def _total_winnings(self) -> int:
        points = list(range(len(self.hands), 0, -1))
        pts = [i[0].bid * i[1] for i in zip(self.sorted_hands, points)]
        return sum(pts)

    def part1(self) -> str | int:
        """Returns total winnings; sum of ranks multiplied by bids."""
        return self._total_winnings()

    def part2(self) -> str | int:
        self.set_joker_rule(True)
        return self._total_winnings()
