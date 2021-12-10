# https://adventofcode.com/2021/day/10


from collections import deque

SCORES_1 = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

SCORES_2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

PAIRS = {
    '{': '}',
    '<': '>',
    '[': ']',
    '(': ')',
}
PAIRS.update({v: k for k, v in PAIRS.items()})

OPENS = frozenset('({[<')


def p1(inpt: str) -> int:
    lines = inpt.splitlines()
    score = 0
    for line in lines:
        stack = deque()
        for char in line:
            if char in OPENS:
                stack.append(char)
            else:
                pair = stack.pop()
                if pair != PAIRS[char]:
                    score += SCORES_1[char]
                    break
    return score


def p2(inpt: str) -> int:
    lines = inpt.splitlines()
    scores = []
    for line in lines:
        stack = deque()
        score = 0
        for char in line:
            if char in OPENS:
                stack.append(char)
            else:
                pair = stack.pop()
                if pair != PAIRS[char]:
                    # Invalid line, ignore
                    break
        else:
            while stack:
                char = stack.pop()
                score = score*5 + SCORES_2[PAIRS[char]]
            scores.append(score)
    scores.sort()
    return scores[len(scores)//2]


if __name__ == "__main__":
    with open('input.txt') as infile:
        data = infile.read()
    print("P1: ", p1(data))
    print("P2: ", p2(data))
