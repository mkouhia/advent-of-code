import pytest

from advent_of_code.y23.day10 import PipeMaze


@pytest.mark.parametrize(
    "maze, path",
    [
        (
            """.....
.S-7.
.|.|.
.L-J.
.....""",
            "S-7|J-L|",
        ),
        (
            """-L|F7
7S-7|
L|7||
-L-J|
L|-JF""",
            "S-7|J-L|",
        ),
        (
            """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""",
            "SJFJF7|L7J--FJL|",
        ),
        (
            """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""",
            "SJFJF7|L7J--FJL|",
        ),
    ],
)
def test_path(maze, path):
    pipe_maze = PipeMaze(maze)

    assert [pipe_maze.maze[i][j] for i, j in list(pipe_maze)] == [i for i in path]


@pytest.mark.parametrize(
    "maze, steps",
    [
        (
            """.....
.S-7.
.|.|.
.L-J.
.....""",
            4,
        ),
        (
            """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""",
            8,
        ),
    ],
)
def test_part1(maze, steps):
    assert PipeMaze(maze).part1() == steps


@pytest.mark.parametrize(
    "maze, points",
    [
        (
            """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""",
            4,
        ),
        (
            """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
""",
            4,
        ),
        (
            """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""",
            8,
        ),
        (
            """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""",
            10,
        ),
    ],
)
def test_part2(maze, points):
    print(maze)
    assert PipeMaze(maze).part2() == points
