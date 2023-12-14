"""https://adventofcode.com/2023/day/12"""

import re
import itertools
from dataclasses import dataclass

from ..base import Puzzle


class HotSprings(Puzzle):

    """Packing of strings in records."""

    def part1(self) -> str | int:
        """Number of possible packing options."""
        records = [
            ConditionRecord.from_string(row)
            for row in self.input_text.strip().splitlines()
        ]
        return sum(record.n_replacements() for record in records)

    def part2(self) -> str | int:
        """Number of possible options, first expanding the pattern."""
        records = [
            ConditionRecord.from_string_part2(row)
            for row in self.input_text.strip().splitlines()
        ]
        return sum(record.n_replacements() for record in records)


@dataclass
class ConditionRecord:

    """A record describing spring condition."""

    spec: str
    groups: list[int]

    records = {}

    @classmethod
    def from_string(cls, spec: str):
        """Create record from specification row."""
        parts = spec.split(" ")
        groups = [int(j) for j in parts[1].split(",")]
        return cls(spec, groups)

    @staticmethod
    def expand_spec(spec: str):
        """Expand specification for part 2."""
        parts = spec.split(" ")
        return f"{'?'.join([parts[0]]*5)} {','.join([parts[1]]*5)}"

    @classmethod
    def from_string_part2(cls, spec: str):
        """Create expanded record from specification row, part 2."""
        spec2 = cls.expand_spec(spec)
        return cls.from_string(spec2)

    @staticmethod
    def group_lengths(cond_spec: str):
        """Calculate lengths of repeating # characters in a string."""
        return [
            len(list(g))
            for k, g in itertools.groupby(cond_spec, key=lambda x: x == "#")
            if k
        ]

    @staticmethod
    def find_possible_locations(spec: str, length: int):
        """Yield locations, where # pattern of length can be placed in spec."""
        pattern = r"(?=[.\?]([\?#]{" + str(length) + r"})[.\?])"
        for match_ in re.finditer(pattern, spec):
            yield match_.start(1), match_.end(1)

    def n_replacements(self):
        """Number of possible replacements."""
        return self._do_replacements("." + self.spec.split(" ")[0] + ".", self.groups)

    @classmethod
    def _do_replacements(cls, spec: str, groups: list[int]) -> int:
        """Perform searching of the possible replacements.

        This is sub-optimal, as the runtime is in the order of seconds.
        Perhaps the approach by first mapping the longest group brings
        too much complexity, and we should just check the string beginning
        from the start.
        """
        if not groups:
            return 0 if "#" in spec else 1

        if (key := (spec, tuple(groups))) in cls.records:
            return cls.records[key]

        if len(spec) < sum(groups) + len(groups) - 1:
            return 0

        longest_grp = max(groups)

        spec_lengths = cls.group_lengths(spec)
        if len(spec_lengths) > 0 and (max(spec_lengths) > longest_grp):
            return 0

        if spec_lengths == groups:
            return 1

        split_idx = groups.index(longest_grp)

        groups_before = groups[:split_idx]
        groups_after = groups[split_idx + 1 :]

        count = 0
        for start, end in cls.find_possible_locations(spec, longest_grp):
            f_before = cls._do_replacements(spec[:start], groups_before)
            if f_before == 0:
                continue
            f_after = cls._do_replacements(spec[end:], groups_after)
            if f_after == 0:
                continue
            count += f_before * f_after

        cls.records[(spec, tuple(groups))] = count
        return count
