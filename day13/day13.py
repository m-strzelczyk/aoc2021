# https://adventofcode.com/2021/day/13
from typing import Set, List, Tuple

Graph = Set[Tuple[int, int]]


def load_input(inpt: str) -> (Graph, List[Tuple[str, int]]):
    paper = set()
    instructions = []
    for line in inpt.splitlines():
        if not line:
            continue
        elif line.startswith("fold"):
            orientation, value = line.split('=')
            instructions.append((orientation[-1], int(value)))
        else:
            x, y = map(int, line.split(','))
            paper.add((x, y))
    return paper, instructions


def fold_x(graph: Graph, x: int) -> Graph:
    new_graph = set()
    for pos in graph:
        if pos[0] > x:
            new_graph.add((x-(pos[0]-x), pos[1]))
        else:
            new_graph.add(pos)
    return new_graph


def fold_y(graph: Graph, y: int) -> Graph:
    new_graph = set()
    for pos in graph:
        if pos[1] > y:
            new_graph.add((pos[0], y - (pos[1] - y)))
        else:
            new_graph.add(pos)
    return new_graph


def p1(inpt: str) -> int:
    paper, instructions = load_input(inpt)
    if instructions[0][0] == 'x':
        return len(fold_x(paper, instructions[0][1]))
    else:
        return len(fold_y(paper, instructions[0][1]))


def p2(inpt: str):
    paper, instructions = load_input(inpt)

    for axis, value in instructions:
        if axis == 'x':
            paper = fold_x(paper, value)
        else:
            paper = fold_y(paper, value)

    max_x = max(x for x, _ in paper)
    max_y = max(y for _, y in paper)

    for y in range(max_y+1):
        for x in range(max_x+1):
            print("💙" if (x, y) in paper else "🖤️", end='')
        print("")
    return


if __name__ == "__main__":
    with open('input.txt') as infile:
        data = infile.read()
    print("P1: ", p1(data))
    print("P2: ", p2(data))
