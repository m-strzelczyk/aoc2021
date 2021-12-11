# https://adventofcode.com/2021/day/11
import itertools
from collections import defaultdict


def neighbors(x: int, y: int) -> (int, int):
    for xi, yi in itertools.product((-1,0,1), (-1,0,1)):
        if xi == yi == 0:
            continue
        yield x+xi, y+yi


def load_octos(inp: str) -> defaultdict:
    octos = defaultdict(lambda: float('-inf'))
    for y, line in enumerate(inp.splitlines()):
        for x, octo in enumerate(line):
            octos[(x,y)] = int(octo)
    return octos


def main(inp: str, steps: int, p2_mode: bool) -> int:
    octos = load_octos(inp)

    flashes = 0
    for turn in range(steps):
        flash = set()
        for pos in itertools.product(range(10), range(10)):
            octos[pos] += 1
            if octos[pos] >= 10:
                flash.add(pos)
        flashes_this_turn = 0
        while flash:
            pos = flash.pop()
            # print(f"Position {pos} flashed with value {octos[pos]}.")
            octos[pos] = float('-inf')
            flashes_this_turn += 1
            flashes += 1
            for npos in neighbors(*pos):
                octos[npos] += 1
                if octos[npos] >= 10:
                    flash.add(npos)
        if p2_mode and flashes_this_turn == 100:
            return turn+1
        for pos in itertools.product(range(10), range(10)):
            if octos[pos] < 0:
                octos[pos] = 0
    return flashes


if __name__ == '__main__':
    with open('input.txt') as infile:
        data = infile.read()
    print("P1: ", main(data, 100, False))
    print("P2: ", main(data, 100000, True))
