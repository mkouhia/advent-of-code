import pytest

from advent_of_code.y23.day05 import Almanac, AlmanacMap, AlmanacMapRow


@pytest.fixture
def sample_input() -> str:
    return """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def test_seeds(sample_input: str):
    assert Almanac(sample_input).seeds == [79, 14, 55, 13]


def test_get_maps(sample_input: str):
    maps = Almanac(sample_input).maps

    assert len(maps) == 7
    assert maps[0] == AlmanacMap(
        [
            AlmanacMapRow(50, 98, 2),
            AlmanacMapRow(52, 50, 48),
        ]
    )


@pytest.mark.parametrize("i", range(4))
def test_map_output(sample_input: str, i: int):
    soils = [81, 14, 57, 13]

    almanac = Almanac(sample_input)
    seeds = almanac.seeds
    seed_to_soil = almanac.maps[0]
    received = [seed_to_soil.get_destination(s) for s in seeds]

    assert received == soils


def test_part1(sample_input: str):
    assert Almanac(sample_input).part1() == 35


@pytest.mark.skip
def test_part2(sample_input: str):
    assert Almanac(sample_input).part2() == ...
