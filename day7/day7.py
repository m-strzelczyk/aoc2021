# https://adventofcode.com/2021/day/7
from collections import defaultdict


def p1(inp: str) -> int:
    crabs = list(map(int, inp.split(',')))
    crabmap = defaultdict(int)

    for crab in crabs:
        crabmap[crab] += 1

    left = 0
    left_crab = 0

    # We "start" at pos -1, so we need to prepare the sum of required fuel properly
    right = sum(crabs) + len(crabs)
    right_crab = len(crabs)

    lowest_score = float('inf')

    for i in range(max(crabs)):
        right -= right_crab
        right_crab -= crabmap[i]

        lowest_score = min(lowest_score, right + left)

        left_crab += crabmap[i]
        left += left_crab

    return lowest_score


def p2(inp: str) -> int:
    crabs = list(map(int, inp.split(',')))
    crabmap = defaultdict(int)
    left_scores = defaultdict(int)
    right_scores = defaultdict(int)

    for crab in crabs:
        crabmap[crab] += 1

    # Going from the left
    fuel_need = 0
    crabs_passed = 0
    for i in range(max(crabs)+1):
        left_scores[i] += left_scores[i-1] + fuel_need
        crabs_passed += crabmap[i]
        fuel_need += crabs_passed

    # Going from the right
    fuel_need = 0
    crabs_passed = 0
    for i in reversed(range(max(crabs)+1)):
        right_scores[i] = right_scores[i+1] + fuel_need
        crabs_passed += crabmap[i]
        fuel_need += crabs_passed

    # Find the minimum
    return min(left_scores[i] + right_scores[i] for i in range(max(crabs)+1))


if __name__ == "__main__":
    with open('input.txt') as infile:
        data = infile.read()
    print("P1: ", p1(data))
    print("P2: ", p2(data))
