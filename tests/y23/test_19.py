from functools import reduce
import pytest

from advent_of_code.y23.day19 import Aplenty, Part, PartRange, Range, Workflow


@pytest.fixture
def sample_input() -> str:
    return """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


def test_workflow():
    flow = Workflow("in", ["s<1351:px", "qqz"])
    part = Part(x=787, m=2655, a=1222, s=2876)
    assert flow.apply(part) == "qqz"


def test_process_parts(sample_input: str):
    aplenty = Aplenty(sample_input)
    assert len(list(aplenty.process_parts())) == 3


@pytest.mark.parametrize(
    "range_, split, first, second",
    [
        ((0, 10), 5, (0, 5), (5, 10)),
        ((0, 10), 0, (None, None), (0, 10)),
        ((0, 10), 10, (0, 10), (None, None)),
    ],
)
def test_range_split(range_, split, first, second):
    assert Range(*range_).split(split) == (Range(*first), Range(*second))


def test_split():
    l = (0, 1, 2, 3, 4, 5)
    prange = PartRange.from_single(0, 6)

    expected = (
        PartRange(x=Range(0, 3), m=Range(0, 6), a=Range(0, 6), s=Range(0, 6)),
        PartRange(x=Range(3, 6), m=Range(0, 6), a=Range(0, 6), s=Range(0, 6)),
    )
    assert prange.split("x<3") == expected


def test_apply_range():
    flow = Workflow.from_string("in{x<3:px,qqz}")
    l = (0, 1, 2, 3, 4, 5)
    prange = PartRange.from_single(0, 6)
    expected = {
        "px": PartRange(x=Range(0, 3), m=Range(0, 6), a=Range(0, 6), s=Range(0, 6)),
        "qqz": PartRange(x=Range(3, 6), m=Range(0, 6), a=Range(0, 6), s=Range(0, 6)),
    }
    assert dict(flow.apply_range(prange)) == expected


def test_split_combinations():
    prange = PartRange.from_single(0, 1000)
    flow = Workflow.from_string("rfg{s<537:gd,x>440:R,A}")

    assert prange.n_combinations() == sum(
        r.n_combinations() for _, r in flow.apply_range(prange)
    )


def test_process_range(sample_input: str):
    aplenty = Aplenty(sample_input)
    ranges_ = {
        cls_: Range(min(vals), max(vals) + 1)
        for cls_ in "xmas"
        if (vals := [getattr(p, cls_) for p in aplenty.parts])
    }
    prange = PartRange(**ranges_)

    accepted_parts = list(aplenty.process_parts())
    accepted_ranges = list(aplenty.process_range(prange))

    for r in accepted_ranges:
        print(r.n_combinations(), r)

    for p in accepted_parts:
        print(p)
        for r in accepted_ranges:
            print(r.contains(p), r)
            if r.contains(p):
                break
        else:
            assert False, f"None of the ranges contain the accepted part {p}"
    assert all([any(r.contains(p) for r in accepted_ranges) for p in accepted_parts])


def test_part1(sample_input: str):
    assert Aplenty(sample_input).part1() == 19114


def test_part2(sample_input: str):
    assert Aplenty(sample_input).part2() == 167409079868000
