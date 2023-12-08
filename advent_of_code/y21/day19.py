"""https://adventofcode.com/2021/day/19"""

import re
from io import StringIO

import numpy as np
from ..base import Puzzle

class BeaconScanner(Puzzle):
    
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.scanners = {}
        
        pattern = r'--- scanner (\d) ---\n((?:-?\d+,-?\d+,-?\d+\n)+)'
        for scanner_s in re.findall(pattern, input_text):
            self.scanners[int(scanner_s[0])] = np.genfromtxt(StringIO(scanner_s[1]), delimiter=',', dtype=int)
            

    def part1(self) -> str | int:
        return super().part1()
    
    def part2(self) -> str | int:
        return super().part2()
