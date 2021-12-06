# https://adventofcode.com/2021/day/6
from collections import defaultdict


def main(inp: str, days: int) -> int:
    # Fish states, maps the day of their reproductive cycle to number of fishes in this cycle
    fish_states = defaultdict(int)
    for fish_state in map(int, inp.split(',')):
        fish_states[fish_state] += 1

    for _ in range(days):
        day_zero = fish_states[0]
        for i in range(8):
            fish_states[i] = fish_states[i+1]
        fish_states[6] += day_zero
        fish_states[8] = day_zero

    return sum(fish_states.values())


if __name__ == '__main__':
    with open('input.txt') as infile:
        data = infile.read()
    print("Part 1:", main(data, 80))
    print("Part 2:", main(data, 256))
    print("Part 3:", main(data, 3650)) # 10 years, because why not :P
