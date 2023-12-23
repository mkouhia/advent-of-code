from io import StringIO
import sys
import pytest

from advent_of_code.y23.day20 import PulsePropagation


@pytest.fixture
def sample_input() -> str:
    return r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""


@pytest.mark.parametrize(
    "input_txt,expected_seq",
    [
        (
            r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""",
            (
                """button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a
""",
            ),
        ),
        (
            r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""",
            (
                """button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -high-> output
b -high-> con
con -low-> output
""",
                """button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
""",
                """button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -low-> output
b -low-> con
con -high-> output
""",
                """button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output
""",
            ),
        ),
    ],
)
def test_output(input_txt: str, expected_seq: tuple[str, ...]):
    f = StringIO()
    comms = PulsePropagation(input_txt)
    comms.set_output(f)

    for expected in expected_seq:
        comms.run_cycle()
        output = f.getvalue()
        assert output == expected
        f.truncate(0)
        f.seek(0)


# def test_x():
#     pp = PulsePropagation(r"""broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output
# """)
#     pp.set_output(sys.stdout)
#     for i in range(9):
#         print(f"{i+1}".center(40, '-'))
#         pp.run_cycle()
#         print(pp._result, pp.get_result())

#     assert False


@pytest.mark.parametrize(
    "input_txt, expected",
    [
        (
            r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""",
            32_000_000,
        ),
        (
            r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""",
            1168_7500,
        ),
    ],
)
def test_part1(input_txt: str, expected):
    assert PulsePropagation(input_txt).part1() == expected


@pytest.mark.skip
def test_part2(sample_input: str):
    assert PulsePropagation(sample_input).part2() == ...
