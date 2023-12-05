"""https://adventofcode.com/2023/day/5"""

import numpy as np
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property

from ..base import Puzzle
from ..helpers import partition_range


@dataclass
class AlmanacMapRow:

    """Row of a almanac map."""

    dest_start: int
    source_start: int
    range_length: int

    @classmethod
    def from_str(cls, source: str):
        """Construct from string in almanac."""
        return cls(*[int(i) for i in source.split(" ")])

    def get_destination(self, source: int) -> int | None:
        """Get mapped destination from source.

        Returns None if the row does not apply to the source.
        """
        if self.source_start <= source < (self.source_start + self.range_length):
            return self.dest_start + (source - self.source_start)
        return None

    def get_destination_ranged(
        self, source_start: int, source_len: int
    ) -> tuple[tuple[int, int], list[tuple[int, int]]]:
        """Get mapped destination range from source range

        Args:
            source_start: Number, which starts source range.
            source_len: Length of source range.

        Returns:
            Tuple (range of destination numbers, list of source ranges that
            remain unmapped). Here ranges are in the same format (start, len)
        """
        partition_with = (self.source_start, self.source_start + self.range_length)
        before, overlap, end = [
            self._full_to_len_range(i)
            for i in partition_range(
                (source_start, source_start + source_len),
                partition_with,
            )
        ]

        # Overlap is the range that can be corverted to dest
        if overlap is None:
            overlap_translated = None
        else:
            overlap_translated = (
                self.dest_start + (overlap[0] - self.source_start),
                overlap[1],
            )

        remaining = [i for i in [before, end] if i is not None]
        return (overlap_translated, remaining)

    @staticmethod
    def _full_to_len_range(range_: tuple[int, int] | None) -> tuple[int, int] | None:
        if range_ is None:
            return None
        return range_[0], range_[1] - range_[0]


@dataclass
class AlmanacMap:

    """One mapping from an almanac."""

    rows: list[AlmanacMapRow]

    def get_destination(self, source: int) -> int:
        """Get mapped destination from source."""
        for row in self.rows:
            dest = row.get_destination(source)
            if dest:
                return dest
        return source

    def get_destination_ranged(
        self, *source_ranges: tuple[int, int]
    ) -> Iterable[tuple[int, int]]:
        """Find ranges in destination space, given almanac mappings.

        If mappings do not apply to ranges, return points unmapped.
        The method may arbitrary amount of return ranges, at least
        amount of source ranges. Destination ranges are not merged.

        Args:
            source_ranges: Tuples of (range_start, range_len).

        Returns:
            Mapped output ranges in format (range_start, range_len).
        """
        unmapped = source_ranges
        for row in self.rows:
            left_unmapped = []
            for candidate_range in unmapped:
                dest, unmapped_cand = row.get_destination_ranged(*candidate_range)
                if dest is not None:
                    yield dest
                left_unmapped.extend(unmapped_cand)
            unmapped = left_unmapped

        # Unmapped ranges
        yield from unmapped


class Almanac(Puzzle):

    """Elf almanac."""

    @cached_property
    def seeds(self) -> list[int]:
        """Seeds in the almanac (part 1)."""
        seed_line = self.input_text[: self.input_text.index("\n")]
        assert seed_line.startswith("seeds: ")
        return [int(i) for i in seed_line[7:].split(" ")]

    @cached_property
    def seeds_ranged(self) -> Iterable[tuple[int, int]]:
        """Seed ranges in the almanac, (start, len) (part 2)."""
        nums = self.seeds

        loc = 0
        while loc + 2 <= len(nums):
            yield (nums[loc], nums[loc + 1])
            loc += 2

    @cached_property
    def maps(self) -> list[AlmanacMap]:
        """Maps in the almanac"""
        maps = []
        data_rows = []
        for row in self.input_text.split("\n")[2:]:
            if row.endswith(":"):
                continue

            if len(row) == 0:
                maps.append(AlmanacMap(data_rows))
                data_rows = []
                continue

            data_rows.append(AlmanacMapRow.from_str(row))

        return maps

    def _follow_path(self, seed: int) -> list[int]:
        maps = self.maps
        source = seed
        for almanac_map in maps:
            dest = almanac_map.get_destination(source)
            source = dest
        return dest

    def _follow_path_range(
        self, seed_range: tuple[int, int]
    ) -> Iterable[tuple[int, int]]:
        maps = self.maps
        source_ranges = [seed_range]
        for almanac_map in maps:
            dest_ranges = almanac_map.get_destination_ranged(*source_ranges)
            source_ranges = dest_ranges
        return dest_ranges

    def part1(self) -> str | int:
        """Returns lowest location that corresponds to the initial seeds."""
        return min(self._follow_path(seed) for seed in self.seeds)

    def part2(self) -> str | int:
        """Returns lowest location that corresponds to the initial seeds."""
        min_value = np.inf
        for seed_range in self.seeds_ranged:
            for dest_range in self._follow_path_range(seed_range):
                if dest_range[0] < min_value:
                    min_value = dest_range[0]
        return min_value
