"""https://adventofcode.com/2023/day/12"""

import re
import itertools
from dataclasses import dataclass

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
    spec: str
    groups: list[int]

    records = {}

    @classmethod
    def from_string(cls, spec: str):
        parts = spec.split(" ")
        groups = [int(j) for j in parts[1].split(",")]
        return cls(spec, groups)

    @staticmethod
    def expand_spec(spec: str):
        parts = spec.split(" ")
        return f"{'?'.join([parts[0]]*5)} {','.join([parts[1]]*5)}"

    @classmethod
    def from_string_part2(cls, spec: str):
        spec2 = cls.expand_spec(spec)
        return cls.from_string(spec2)
    
    @staticmethod
    def group_lengths(cond_spec: str):
        return [
            len(list(g))
            for k, g in itertools.groupby(cond_spec, key=lambda x: x == "#")
            if k
        ]
    
    @staticmethod
    def find_possible_locations(spec: str, length: int):
        # for m in re.finditer(rf'(?=([^\.]{{{spring}}}[^#]))', condition):
        #     i = m.span(1)[0]
        #     print(i, condition[:i])
        #     if '#' in condition[:i]:
        #         break
        #     yield m.start(1), m.end(1)#condition[i + spring + 1:]
        pattern = r'(?=[.\?]([\?#]{' + str(length) + r'})[.\?])'
        for match_ in re.finditer(pattern, spec):
            yield match_.start(1), match_.end(1)
            
    def n_replacements(self):
        return self._do_replacements('.' + self.spec.split(' ')[0] + '.', self.groups)

    @classmethod
    def _do_replacements(cls, spec: str, groups: list[int]) -> int:
        if not groups:
            return "#" not in spec
        
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

        if len(groups) == 1:
            count = sum(1 for _ in cls.find_possible_locations(spec, longest_grp))
            return count

        split_idx = groups.index(longest_grp)

        groups_before = groups[:split_idx]
        groups_after = groups[split_idx+1:]
        

        count = 0
        for start, end in cls.find_possible_locations(spec, longest_grp):
            # Find out if it is possible to create matches with this split
            
            
            f_before = cls._do_replacements(spec[:start], groups_before)# if groups_before else 1
            if f_before == 0:
                continue
            f_after = cls._do_replacements(spec[end:], groups_after)# if groups_after else 1
            if f_after == 0:
                continue
            count += f_before * f_after

        cls.records[(spec, tuple(groups))] = count
        return count
