"""https://adventofcode.com/2023/day/19"""

from collections.abc import Iterable
from dataclasses import dataclass

from ..base import Puzzle


@dataclass
class Part:

    """Part from Machine island part machine."""

    x: int
    m: int
    a: int
    s: int

    def sum_rating(self):
        """Sum of XMAS ratings."""
        return self.x + self.m + self.a + self.s

    @classmethod
    def from_string(cls, s):
        """Create part from string specification."""
        return cls(**{p[0]: int(p[2:]) for p in s.strip("{}").split(",")})

    def evaluate(self, condition: str) -> bool:
        """Evaluate if condition applies.

        Args:
            condition: Simple equation, such as 'a<2005.

        Returns
            Moolean values, whether condition is true or false."""
        attr_name = condition[0]
        comp = condition[1]
        value = int(condition[2:])
        if comp == "<":
            return getattr(self, attr_name) < value
        if comp == ">":
            return getattr(self, attr_name) > value
        raise NotImplementedError


class Workflow:

    """Elf machine workflow."""

    def __init__(self, name: str, rules: list[str]) -> None:
        self.name = name
        self.rules = rules

    @classmethod
    def from_string(cls, s):
        """Initiate workflow from string specification"""
        name = s[: s.index("{")]
        rules = s[s.index("{") + 1 : -1].split(",")
        return cls(name, rules)

    def apply(self, part: Part) -> str:
        """Apply workflow ruleset to part. Return target that applies."""
        for rule in self.rules:
            if ":" not in rule:
                return rule
            condition, target = rule.split(":")
            if part.evaluate(condition):
                return target
        print(self.name, self.rules, part)
        raise NotImplementedError


class Aplenty(Puzzle):

    """Help elves sort out parts with rules."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        workflows, parts = [
            block.splitlines() for block in input_text.strip().split("\n\n")
        ]

        self.workflows = {
            w.name: w for i in workflows if (w := Workflow.from_string(i))
        }
        self.parts = [Part.from_string(s) for s in parts]

    def process_parts(self) -> Iterable[Part]:
        """Put parts through workflows, return accepted parts."""
        for part in self.parts:
            target = "in"
            while target not in ["R", "A"]:
                flow = self.workflows[target]
                target = flow.apply(part)
            if target == "A":
                yield part

    def part1(self) -> str | int:
        """Sum of rating numbers for all accepted parts."""
        return sum(p.sum_rating() for p in self.process_parts())

    def part2(self) -> str | int:
        return super().part2()
