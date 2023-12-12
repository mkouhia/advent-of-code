"""https://adventofcode.com/2023/day/12"""

import re
import itertools
from dataclasses import dataclass

import numpy as np

from ..base import Puzzle


class HotSprings(Puzzle):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)

    def part1(self) -> str | int:
        records = [
            ConditionRecord.from_string(row)
            for row in self.input_text.strip().splitlines()
        ]
        return sum(record.n_replacements() for record in records)

    def part2(self) -> str | int:
        records = [
            ConditionRecord.from_string_part2(row)
            for row in self.input_text.strip().splitlines()
        ]
        return sum(record.n_replacements() for record in records)


@dataclass
class ConditionRecord:
    condition: np.array
    mask: np.array
    groups: list[int]
    spec: str


    @classmethod
    def from_string(cls, spec: str):
        parts = spec.split(" ")
        cond_str = parts[0]
        groups = [int(j) for j in parts[1].split(",")]
        condition = np.array([c == "#" for c in cond_str])
        mask = np.array([c == "?" for c in cond_str])
        return cls(condition, mask, groups, spec)

    @staticmethod
    def expand_spec(spec: str):
        parts = spec.split(" ")
        return f"{'?'.join([parts[0]]*5)} {','.join([parts[1]]*5)}"

    @classmethod
    def from_string_part2(cls, spec: str):
        spec2 = cls.expand_spec(spec)
        return cls.from_string(spec2)
    
    @property
    def is_valid(self):
        found_counts = [
            len(list(g))
            for k, g in itertools.groupby(self.condition, key=lambda x: x == "#")
            if k
        ]
        return found_counts == self.groups
    
    @staticmethod
    def find_possible_locations(spec: str, length: int):
        pattern = r'(?=((^|[\.\?])[\?#]{' + length + '}($|[\.\?])))'
        for match in re.finditer(pattern, spec):
            yield match.start(1), match.end(1)

    @classmethod
    def do_replacements(cls, spec: str, groups: list[int]) -> int:

        longest_grp = max(groups)

        if len(groups) == 1:
            # Return number of possible placements for this item
            return len(cls.find_possible_locations(spec, longest_grp))

        split_idx = groups.index(longest_grp)

        groups_before = groups[:split_idx]
        groups_after = groups[split_idx+1:]

        count = 0
        for start, end in cls.find_possible_locations(spec, longest_grp):
            # TODO find out if it is possible to create matches with this split
            f_before = cls.do_replacements(spec[:start], groups_before) if groups_before else 1
            f_after = cls.do_replacements(spec[end:], groups_after) if groups_after else 1
            count += f_before * f_after

        return count

    def n_replacements(self):
        num_unknown = np.sum(self.mask)
        replacements = np.array(list(itertools.product(range(2), repeat=num_unknown)))
        n_opts = len(replacements)

        alternatives = np.tile(self.condition, (n_opts, 1))
        alternatives[:, self.mask] = replacements

        return self._evaluate_cond_2d(alternatives)

    def _evaluate_cond_2d(self, alts):
        vcol = np.full((len(alts), 1), False)
        cond = np.hstack((vcol, alts, vcol))

        leading = np.nonzero(~cond[:, :-1] & cond[:, 1:])
        trailing = np.nonzero(cond[:, :-1] & ~cond[:, 1:])

        diffs = np.vstack((trailing[1], -leading[1])).sum(axis=0)
        opts = np.split(diffs, np.unique(leading[0], return_index=True)[1][1:])

        return sum(1 for i in opts if i.tolist() == self.groups)
