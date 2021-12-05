# https://adventofcode.com/2021/day/5
import re
from collections import defaultdict

LINE_RE = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')


def main(inp: str, diagonals: bool) -> int:
    field = defaultdict(int)
    for line in inp.splitlines():
        match = LINE_RE.match(line)
        x1, y1, x2, y2 = map(int, match.groups())
        if x1 == x2:
            for i in range(min(y1, y2), max(y1, y2)+1):
                field[(x1, i)] += 1
        elif y1 == y2:
            for i in range(min(x1, x2), max(x1, x2) + 1):
                field[(i, y1)] += 1
        elif diagonals:
            # The diagonal, only for part 2
            range_x = range(min(x1, x2), max(x1, x2)+1)
            if x1 < x2:
                range_x = reversed(range_x)
            range_y = range(min(y1, y2), max(y1, y2)+1)
            if y1 < y2:
                range_y = reversed(range_y)
            for (x, y) in zip(range_x, range_y):
                field[(x, y)] += 1
    count = 0
    for value in field.values():
        if value >= 2:
            count += 1
    return count


if __name__ == "__main__":
    with open('input.txt') as infile:
        data = infile.read()
    print('P1: ', main(data, False))
    print('P2: ', main(data, True))
