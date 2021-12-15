# https://adventofcode.com/2021/day/15
import heapq
import itertools
from collections import defaultdict
from typing import Tuple


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Heap:
    def __init__(self):
        self._store = []

    def push(self, item):
        heapq.heappush(self._store, item)

    def pop(self):
        return heapq.heappop(self._store)

    def __bool__(self):
        return bool(self._store)


def neighbors(x: int, y: int) -> Tuple[int, int]:
    yield x+1, y
    yield x, y+1
    yield x-1, y
    yield x, y-1


def load_input(inpt: str):
    cave_map = defaultdict(lambda: float('inf'))
    for y, line in enumerate(inpt.splitlines()):
        for x, risk in enumerate(line):
            cave_map[(x, y)] = int(risk)
    return cave_map, x, y


def print_best_path(cave_map: defaultdict, best_path: dict, end: tuple):
    max_x, max_y = end

    it = end
    the_path = {it}
    while it != (0, 0):
        it = best_path[it]
        the_path.add(it)

    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x, y) in the_path:
                print(f"{bcolors.FAIL}{cave_map[(x, y)]}{bcolors.ENDC}", end='')
            else:
                print(cave_map[(x, y)], end='')
        print('')
    return 0


def main(inpt: str, p2_mode: bool) -> int:
    cave_map, max_x, max_y = load_input(inpt)
    travel_cost = defaultdict(lambda: float('inf'))
    best_path = {}

    start = (0, 0)
    travel_cost[start] = 0

    if p2_mode:
        len_x = max_x+1
        len_y = max_y+1
        for x, y in itertools.product(range(5), range(5)):
            for ix, iy in itertools.product(range(len_x), range(len_y)):
                cave_map[(ix+x*len_x, iy+y*len_y)] = (cave_map[(ix, iy)] + x + y - 1) % 9 + 1
                print((ix+x*len_x, iy+y*len_y))

        max_x = len_x*5 - 1
        max_y = len_y*5 - 1

    end = (max_x, max_y)
    nav_heap = Heap()
    nav_heap.push((0, start))

    while True:
        cost, pos = nav_heap.pop()
        if pos == end:
            print_best_path(cave_map, best_path, end)
            return cost
        if cost == float('inf'):
            continue
        for neighbor in neighbors(*pos):
            new_cost = cost + cave_map[neighbor]
            if new_cost < travel_cost[neighbor]:
                best_path[neighbor] = pos
                travel_cost[neighbor] = new_cost
                nav_heap.push((new_cost, neighbor))


if __name__ == '__main__':
    with open('example.txt') as infile:
        data = infile.read()
    print('P1: ', main(data, False))
    print('P2: ', main(data, True))
