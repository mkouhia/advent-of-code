import pytest

from advent_of_code.y23.day25 import Snowverload


@pytest.fixture
def sample_input() -> str:
    return """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""


def test_part1(sample_input: str):
    assert Snowverload(sample_input).part1() == 54


@pytest.mark.skip
def test_part2(sample_input: str):
    assert Snowverload(sample_input).part2() == ...
