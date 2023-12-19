"""https://adventofcode.com/2023/day/19"""

import operator
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

    def __str__(self) -> str:
        parts = [f"{att}={getattr(self, att)}" for att in "xmas"]
        return f'{{{",".join(parts)}}}'


@dataclass(frozen=True)
class PartRange:
    x: tuple[int, ...]
    m: tuple[int, ...]
    a: tuple[int, ...]
    s: tuple[int, ...]

    def split(self, condition: str) -> tuple["PartRange", "PartRange"]:
        """Split part range by condition.

        Args:
            condition: Simple equation, such as 'a<2005.

        Returns:
            Two ranges: first, the range for which the equation is true,
            then the parts that do not apply to this range.
        """
        attr_name = condition[0]
        comp = condition[1]
        value = int(condition[2:])
        assert comp in "<>"
        oper = operator.lt if comp == "<" else operator.gt
        accept: list[int] = [i for i in getattr(self, attr_name) if oper(i, value)]
        discard: list[int] = [i for i in getattr(self, attr_name) if not oper(i, value)]

        other_attr = {n: getattr(self, n) for n in "xmas" if n != attr_name}

        trues = PartRange(**{attr_name: tuple(accept)} | other_attr) if accept else None
        falses = (
            PartRange(**{attr_name: tuple(discard)} | other_attr) if discard else None
        )
        return trues, falses

    @classmethod
    def from_single(cls, iterable_):
        nums_ = tuple(list(iterable_))
        return cls(x=nums_, m=nums_, a=nums_, s=nums_)

    def n_combinations(self):
        """Returns amount of distinct part combinations"""
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)

    def contains(self, part: Part) -> bool:
        """Part is in part range."""
        return (
            part.x in self.x
            and part.m in self.m
            and part.a in self.a
            and part.s in self.s
        )


class Workflow:

    """Elf machine workflow."""

    def __init__(self, name: str, rules: list[str]) -> None:
        self.name = name
        self.rules = rules

    def __str__(self) -> str:
        return f'{self.name}{{{",".join(self.rules)}}}'

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
        raise NotImplementedError

    def apply_range(self, prange: PartRange) -> Iterable[tuple[str, PartRange]]:
        """Apply workflow ruleset to part range.

        Yields:
            Tuples of target to splitted part range.
        """
        ret = {}
        range_remains = prange
        for rule in self.rules:
            if ":" not in rule:
                yield (rule, range_remains)
                break
            condition, target = rule.split(":")
            accepted, rejected = range_remains.split(condition)
            yield (target, accepted)
            range_remains = rejected
        return ret


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

    def process_range(self, part_range: PartRange) -> Iterable[PartRange]:
        """Put part ranges through workflows, return ranges that end accepted."""
        targets = {"in": part_range}
        while targets:
            next_key = next(iter(targets.keys()))
            prange = targets.pop(next_key)
            flow = self.workflows[next_key]

            for target_, range_ in flow.apply_range(prange):
                if target_ == "R" or range_ is None:
                    continue
                elif target_ == "A":
                    yield range_
                elif target_ not in targets:
                    targets[target_] = range_
                else:
                    raise NotImplementedError

    def part1(self) -> str | int:
        """Sum of rating numbers for all accepted parts."""
        return sum(p.sum_rating() for p in self.process_parts())

    def part2(self) -> str | int:
        prange = PartRange.from_single(range(1, 4001))
        return sum(r.n_combinations() for r in self.process_range(prange))
