"""https://adventofcode.com/2023/day/13"""

from collections.abc import Iterable

from ..base import Puzzle

class PointOfIncidence(Puzzle):
    
    def part1(self) -> str | int:
        patterns = self.input_text.strip().split('\n\n')
        total = 0
        for pat_txt in patterns:
            pat = Pattern(pat_txt)
            total += 100*pat.mirror_row() + pat.mirror_col()
        return total
    
    def part2(self) -> str | int:
        return super().part2()

def mirror_point(elements: Iterable):
    break_order = sorted(range(1, len(elements)), key=lambda k: abs(len(elements)/2-k))
    for breakpoint in break_order:
        if _is_mirrored(elements, breakpoint):
            return breakpoint
    return 0

def _is_mirrored(text: Iterable, breakpoint: int) -> tuple[int, int]:
    return all(map(lambda p: p[0] == p[1], zip(text[:breakpoint][::-1], text[breakpoint:])))

class Pattern:

    def __init__(self, text) -> None:
        self.text = text
        self.row_strings = text.splitlines()
        self.col_strings = [''.join(col) for col in zip(*self.row_strings)]

    def mirror_col(self):
        return mirror_point(self.col_strings)
    
    def mirror_row(self):
        return mirror_point(self.row_strings)
