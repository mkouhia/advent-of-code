import pytest

from advent_of_code.y23.day17 import ClumsyCrucible, dijkstra_algorithm
from advent_of_code.helpers import highlight_by_pos

@pytest.fixture
def sample_input() -> str:
    return """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


def test_graph():
    s = """123\n456"""
    expected = {
        (0, 0): [((0, 1), 2), ((1, 0), 4)],
        (0, 1): [((0, 0), 1), ((0, 2), 3), ((1, 1), 5)],
        (0, 2): [((0, 1), 2), ((1, 2), 6)],
        (1, 0): [((1, 1), 5), ((0, 0), 1)],
        (1, 1): [((1, 0), 4), ((1, 2), 6), ((0, 1), 2)],
        (1, 2): [((1, 1), 5), ((0, 2), 3)],
    }
    assert ClumsyCrucible(s).construct_graph() == expected

def test_dijkstra(sample_input):
    maze = ClumsyCrucible(sample_input)
    graph = maze.construct_graph()
    dist, prev = dijkstra_algorithm(graph, start_node=(0,0))
    
    path_to_end = []
    node_ = (maze.shape[0] - 1, maze.shape[1] - 1)
    while node_ != (0,0):
        path_to_end.append(node_)
        node_ = prev[node_]
        
    print(path_to_end)
    s = highlight_by_pos(sample_input, path_to_end)
    print(s)
    assert dist[path_to_end[0]] == 102

@pytest.mark.skip
def test_part1(sample_input: str):
    assert ClumsyCrucible(sample_input).part1() == 102


@pytest.mark.skip
def test_part2(sample_input: str):
    assert ClumsyCrucible(sample_input).part2() == ...
