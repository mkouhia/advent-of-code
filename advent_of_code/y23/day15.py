"""https://adventofcode.com/2023/day/15"""

from ..base import Puzzle


class LensLibrary(Puzzle):

    """Machine in lava production facility."""

    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.initialization_seq = input_text.replace("\n", "")
        self.steps = self.initialization_seq.split(",")
        self.boxes = [{} for _ in range(256)]

    @staticmethod
    def hash_(string: str) -> int:
        """Holiday ASCII String Helper algorithm (appendix 1A)."""
        current_value = 0
        for char_ in string:
            current_value = ((current_value + ord(char_)) * 17) % 256
        return current_value

    def state_str(self):
        """Print status in boxes at current state."""
        ret = []
        for box_i, box in enumerate(self.boxes):
            if len(box) > 0:
                lenses = " ".join(f"[{label} {num}]" for label, num in box.items())
                ret.append(f"Box {box_i}: {lenses}")

        return "\n".join(ret)

    def perform_step(self, step):
        """Perform step in the initialization sequence."""
        if "=" in step:
            label, num = step.split("=")
            box_id = self.hash_(label)
            self.boxes[box_id][label] = int(num)
        else:
            assert step.endswith("-")
            label = step[:-1]
            box_id = self.hash_(label)
            self.boxes[box_id].pop(label, None)

    def part1(self) -> str | int:
        """Returns sum of hashes in each steps in initialization sequence."""
        return sum(self.hash_(step) for step in self.steps)

    def part2(self) -> str | int:
        """Returns the focusing power of the resulting lens configuration."""
        for step in self.steps:
            self.perform_step(step)

        return sum(
            (box_i + 1) * (slot_i + 1) * f_length
            for box_i, box in enumerate(self.boxes)
            for slot_i, f_length in enumerate(box.values())
        )
