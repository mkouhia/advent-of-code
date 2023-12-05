"""https://adventofcode.com/2023/day/5"""

from dataclasses import dataclass
from functools import cached_property

from ..base import Puzzle


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


class Almanac(Puzzle):

    """Elf almanac."""

    @cached_property
    def seeds(self) -> list[int]:
        """Seeds in the almanac."""
        seed_line = self.input_text[: self.input_text.index("\n")]
        assert seed_line.startswith("seeds: ")
        return [int(i) for i in seed_line[7:].split(" ")]

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

    def part1(self) -> str | int:
        """Returns lowest location that corresponds to the initial seeds."""
        return min(self._follow_path(seed) for seed in self.seeds)

    def part2(self) -> str | int:
        return ...
