# https://adventofcode.com/2021/day/8


#  0    A
# 1 2  B C
#  3    D
# 4 5  E F
#  6    G
from collections import defaultdict


def p1(inpt: str) -> int:
    cnt = 0
    for line in inpt.splitlines():
        line = line.split("|")[1].strip().split()
        for word in line:
            if len(word) in {2,3,4,7}:
                cnt += 1
    return cnt


def decode_letters(letters: str) -> dict:
    words = letters.split()
    d = {}
    for word in words:
        if len(word) == 2:
            d[1] = frozenset(word)
        elif len(word) == 3:
            d[7] = frozenset(word)
        elif len(word) == 4:
            d[4] = frozenset(word)
        elif len(word) == 7:
            d[8] = frozenset(word)

    letter_count = defaultdict(int)
    for letter in letters:
        letter_count[letter] += 1
    del letter_count[' ']
    print(letter_count)

    segments = {}
    segments['a'] = list(d[7].difference(d[1]))[0]

    one_1, one_2 = d[1]
    if letter_count[one_1] == 8:
        segments['c'] = one_1
        segments['f'] = one_2
    else:
        segments['c'] = one_2
        segments['f'] = one_1

    four_1, four_2 = d[4].difference(d[1])
    if letter_count[four_1] == 6:
        segments['b'] = four_1
        segments['d'] = four_2
    else:
        segments['b'] = four_2
        segments['d'] = four_1

    for word in words:
        if len(word) == 6:
            if len(set(word).difference(d[7]).difference(d[4])) == 1:
                segments['g'] = set(word).difference(d[7]).difference(d[4]).pop()
                d[9] = frozenset(word)

    segments['e'] = list(d[8].difference(d[9]))[0]

    d[0] = d[8].difference({segments['d']})
    d[2] = frozenset([segments['a'], segments['c'], segments['d'], segments['e'], segments['g']])
    d[3] = frozenset([segments['a'], segments['c'], segments['d'], segments['f'], segments['g']])
    d[5] = frozenset([segments['a'], segments['b'], segments['d'], segments['f'], segments['g']])
    d[6] = frozenset([segments['a'], segments['b'], segments['d'], segments['e'], segments['f'], segments['g']])

    return {v: k for k, v in d.items()}


def process_output(output: str, d: dict) -> int:
    l1, l2, l3, l4 = output.split()
    return 1000*d[frozenset(l1)] + 100*d[frozenset(l2)] + 10*d[frozenset(l3)] + d[frozenset(l4)]


def p2(inpt: str) -> int:
    result = 0
    for line in inpt.splitlines():
        letters, output = line.split("|")
        d = decode_letters(letters)
        result += process_output(output, d)
    return result


if __name__ == '__main__':
    with open('input.txt') as infile:
        data = infile.read()
    print("P1: ", p1(data))
    print("P2: ", p2(data))
