"""https://adventofcode.com/2023/day/20"""

from abc import ABC, abstractmethod
from collections import deque, namedtuple
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
import sys

from advent_of_code.helpers import ResultCycler
from ..base import Puzzle


class Signal(Enum):
    low = -1
    high = 1


@dataclass
class Message:
    to_: str
    from_: str
    signal: Signal

    def __repr__(self) -> str:
        return f"{self.from_} -{self.signal.name}-> {self.to_}"


class MessageQueue:
    def __init__(self, out_file=None) -> None:
        self.queue: deque[Message] = deque([])
        self.connected: dict[str, Module] = {}
        self.out_file = out_file

    def make_inverse_connections(self):
        conj_back = {
            n: [] for n, mod in self.connected.items() if isinstance(mod, Conjunction)
        }
        for source, mod in self.connected.items():
            for target in conj_back:
                if target in mod.destinations:
                    self.connected[target].declare_input(source)

    def subscribe(self, module: "Module"):
        self.connected[module.name] = module
        module.connect(self)

    def publish(self, message: Message):
        self.queue.append(message)
        if self.out_file is not None:
            self.out_file.write(str(message) + "\n")

    def run(self) -> tuple[int, int]:
        n_high, n_low = 0, 0
        while self.queue:
            message = self.queue.popleft()
            if message.to_ in self.connected:
                self.connected[message.to_].process(message)

            if message.signal is Signal.high:
                n_high += 1
            else:
                n_low += 1
        return n_high, n_low


class PulsePropagation(Puzzle, ResultCycler):
    def __init__(self, input_text: str) -> None:
        super().__init__(input_text)
        self.messages = MessageQueue()
        self.modules = {
            mod.name: mod
            for s in input_text.strip().splitlines()
            if (mod := Module.from_string(s))
        }
        self._result: tuple[int, int] = (0, 0)

        for module in self.modules.values():
            self.messages.subscribe(module)

        self.messages.make_inverse_connections()

        self.button = Broadcaster("button", "broadcaster")
        self.button.connect(self.messages)

    def __hash__(self):
        val = hash(self.input_text)
        for k in [self._result] + list(self.modules.values()):
            val += (hash(k) + 13) * 7
        return val

    def get_result(self):
        return complex(*self._result)

    def set_output(self, out_file):
        self.messages.out_file = out_file

    def run_cycle(self) -> tuple[int, int]:
        message = Message("broadcaster", "button", Signal.low)
        self.messages.publish(message)
        self._result = self.messages.run()
        return self._result

    def part1(self) -> str | int:
        val_ = self.find_result_after(1000, cumulative=True)
        return int(val_.real * val_.imag)

    def part2(self) -> str | int:
        return super().part2()


class Module(ABC):
    _prefix = ""

    def __init__(self, name: str, *destinations: str) -> None:
        self.name = name
        self.destinations = destinations
        self.out_queue: MessageQueue = None

    def __repr__(self) -> str:
        return f"{self._prefix}{self.name} -> {', '.join(self.destinations)}"

    def __hash__(self) -> str:
        return hash(self.__repr__())

    @abstractmethod
    def process(self, message: Message):
        ...

    def connect(self, queue: MessageQueue):
        self.out_queue = queue

    def _send_all(self, signal: Signal):
        for receiver in self.destinations:
            message = Message(receiver, self.name, signal)
            self.out_queue.publish(message)

    @classmethod
    def from_string(self, spec: str):
        parts = spec.split(" -> ")
        name = parts[0]
        destinations = parts[1].split(", ")
        if name.startswith("%"):
            return FlipFlop(name[1:], *destinations)
        if name.startswith("&"):
            return Conjunction(name[1:], *destinations)
        return Broadcaster(name, *destinations)


class Broadcaster(Module):
    _prefix = ""

    def process(self, message: Message):
        self._send_all(message.signal)


class FlipFlop(Module):
    _prefix = "%"

    def __init__(self, name: str, *destinations: str) -> None:
        super().__init__(name, *destinations)
        self.state = -1

    def __hash__(self) -> str:
        return super().__hash__() + 7 * hash(self.state)

    def process(self, message: Message):
        if message.signal is Signal.high:
            # Ignore signal, nothing happens
            return

        self.state = -self.state
        sig = Signal.high if self.state == 1 else Signal.low
        self._send_all(sig)


class Conjunction(Module):
    _prefix = "&"

    def __init__(self, name: str, *destinations: str) -> None:
        super().__init__(name, *destinations)
        self.memory: dict[str, Signal] = {}

    def __hash__(self) -> str:
        return super().__hash__() + 7 * hash(tuple(self.memory.items()))

    def declare_input(self, input_name: str):
        self.memory[input_name] = Signal.low

    def process(self, message: Message):
        self.memory[message.from_] = message.signal
        sig = (
            Signal.low
            if all(sig is Signal.high for sig in self.memory.values())
            else Signal.high
        )
        self._send_all(sig)
