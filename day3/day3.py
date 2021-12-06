# https://adventofcode.com/2021/day/3

def p1(input: str) -> int:
    input = input.strip().splitlines()
    line_count = len(input)
    bits = [0]*len(input[0])
    for line in input:
        for i, bit in enumerate(line):
            bits[i] += 1 if bit == '1' else 0
    print(bits)
    gamma = int("".join('1' if i > line_count/2 else '0' for i in bits), 2)
    epsilon = int("".join('1' if i <= line_count/2 else '0' for i in bits), 2)
    print(gamma, epsilon)
    return gamma * epsilon

################################################################################


def filter_zeros_ones(lines: set, pos: int) -> (set, set):
    zeros, ones = set(), set()
    for line in lines:
        if line[pos] == '1':
            ones.add(line)
        else:
            zeros.add(line)
    return zeros, ones


def p2(input: str) -> int:
    input = input.strip().splitlines()

    oxygen, carbon = set(input), set(input)

    for i in range(len(input[0])):
        zeros, ones = filter_zeros_ones(oxygen, i)
        oxygen = zeros if len(zeros) > len(ones) else ones
        if len(oxygen) == 1:
            break

    for i in range(len(input[0])):
        zeros, ones = filter_zeros_ones(carbon, i)
        carbon = zeros if len(zeros) <= len(ones) else ones
        if len(carbon) == 1:
            break

    oxygen, carbon = oxygen.pop(), carbon.pop()
    print(oxygen, carbon)
    oxygen = int(oxygen, 2)
    carbon = int(carbon, 2)
    return oxygen * carbon