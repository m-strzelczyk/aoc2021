# https://adventofcode.com/2021/day/9
import collections
import itertools
from collections import defaultdict, deque


def prepare_field(inp: str) -> (defaultdict, int, int):
    field = defaultdict(lambda: 9)
    for y, line in enumerate(inp.splitlines()):
        for x, digit in enumerate(line):
            field[(x, y)] = int(digit)
    max_x = len(inp.splitlines()[0])
    max_y = len(inp.splitlines())

    return field, max_x, max_y


def neighbors(x: int, y: int) -> (int, int):
    yield x+1, y
    yield x, y + 1
    yield x-1, y
    yield x, y-1


def p1(inp: str) -> int:
    field, max_x, max_y = prepare_field(inp)

    result = 0

    for x, y in itertools.product(range(max_x), range(max_y)):
        v = field[(x, y)]
        for pos in neighbors(x, y):
            if v >= field[pos]:
                break
        else:
            result += v + 1

    return result


def flood_basin(field, x, y, basins):
    basin_id = id((x, y))
    queue = deque()
    queue.append((x, y))
    while queue:
        pos = queue.popleft()
        if field[pos] == 9:
            continue

        if basins[pos] == basin_id:
            continue
        else:
            assert basins[pos] is None

        basins[pos] = basin_id
        queue.extend(neighbors(*pos))


def p2(inp: str) -> int:
    field, max_x, max_y = prepare_field(inp)
    basins = defaultdict(lambda: None)

    for x, y in itertools.product(range(max_x), range(max_y)):
        if field[(x, y)] == 9:
            continue
        if basins[(x, y)] is not None:
            continue
        flood_basin(field, x, y, basins)

    counter = collections.Counter(basins.values())
    b1, b2, b3 = counter.most_common(3)
    return b1[1] * b2[1] * b3[1]


if __name__ == '__main__':
    with open('input.txt') as infile:
        data = infile.read()
    print('P1: ', p1(data))
    print('P2: ', p2(data))
