# https://adventofcode.com/2021/day/12
from collections import defaultdict
from typing import List, Dict, Set


def build_graph(inpt: str) -> Dict[str, Set[str]]:
    graph = defaultdict(set)
    for line in inpt.splitlines():
        start, end = line.strip().split('-')
        graph[start].add(end)
        graph[end].add(start)
    return graph


def p1_condition(path_so_far: List[str], cave: str, _: Dict[str, int]):
    return (cave.islower() and cave not in path_so_far) or cave.isupper()


def p2_condition(_: List[str], cave: str, visit_counter: Dict[str, int]):
    if cave == "start":
        return False
    if cave.isupper():
        return True
    if any(value > 1 and key.islower() for key, value in visit_counter.items()) and visit_counter[cave]:
        return False
    return True


def traverse(graph: Dict[str, Set[str]], path_so_far: List[str], visit_counter: Dict[str, int], condition):
    current_pos = path_so_far[-1]
    if current_pos == 'end':
        yield ",".join(path_so_far)
        return

    for neighbor in graph[current_pos]:
        # print(f"Path so far {path_so_far}, want to go: {neighbor}, counter: {visit_counter}, "
        #       f"result {condition(path_so_far, neighbor, visit_counter)}")
        if condition(path_so_far, neighbor, visit_counter):
            yield from traverse(graph, [*path_so_far, neighbor],
                                defaultdict(int, **{**visit_counter, neighbor: visit_counter[neighbor]+1}),
                                condition)

    return


def p1(inpt: str) -> int:
    graph = build_graph(inpt)
    visit_counter = defaultdict(int)
    cnt = 0
    for path in traverse(graph, ['start'], visit_counter, p1_condition):
        # print(path)
        cnt += 1

    return cnt


def p2(inpt: str) -> int:
    graph = build_graph(inpt)
    visit_counter = defaultdict(int, start=1)
    cnt = 0
    for path in traverse(graph, ['start'], visit_counter, p2_condition):
        # print(path)
        cnt += 1

    return cnt


if __name__ == "__main__":
    with open('input.txt') as infile:
        data = infile.read()
    print("P1: ", p1(data))
    print("P2: ", p2(data))
