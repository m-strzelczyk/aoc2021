# https://adventofcode.com/2021/day/14
from typing import Tuple, Dict
from collections import Counter


def load_input(inpt: str) -> Tuple[str, Dict[str, str]]:
    start, *rest = inpt.splitlines()
    polmap = {}
    for line in rest[1:]:
        pair, insert = line.split(' -> ')
        polmap[pair] = insert
    return start, polmap


def p1(inpt: str, steps: int) -> int:
    start, polmap = load_input(inpt)

    pairs = Counter()
    for i in range(len(start)-1):
        pairs[start[i:i+2]] += 1
    for _ in range(steps):
        new_pairs = Counter()
        for pair, count in pairs.items():
            left, right = pair
            middle = polmap[pair]
            new_pairs[left+middle] += count
            new_pairs[middle+right] += count
        pairs = new_pairs

    elelemt_count = Counter()
    for (left, right), count in pairs.items():
        elelemt_count[left] += count
        elelemt_count[right] += count

    # Since the letters at the start and end of the protein
    # are the only ones that aren't present in 2 pairs,
    # we add 1 to their count, so then we can properly divide
    # their count in half.
    elelemt_count[start[0]] += 1
    elelemt_count[start[-1]] += 1

    most_common = max(elelemt_count.values())//2
    least_common = min(elelemt_count.values())//2

    return most_common - least_common


if __name__ == '__main__':
    with open('input.txt') as infile:
        data = infile.read()
    print('P1: ', p1(data, 10))
    print('P2: ', p1(data, 40))
