# https://adventofcode.com/2021/day/4
import dataclasses
from typing import List


@dataclasses.dataclass
class Field:
    value: int
    marked: bool


class Board:
    fields: List[List[Field]]
    value_to_position: dict[(int, int)]
    size: int

    def __init__(self, board_input: List[str]):
        self.fields = []
        self.value_to_position = {}
        for y, line in enumerate(board_input):
            row = []
            for x, value in enumerate(line.split()):
                row.append(Field(int(value), False))
                self.value_to_position[int(value)] = (x, y)
            self.fields.append(row)
        self.size = len(self.fields[0])

    def mark(self, value: int) -> bool:
        """
        Mark a field, return True if the board is winning.
        """
        try:
            x, y = self.value_to_position[value]
        except KeyError:
            return False
        self.fields[y][x].marked = True
        # Horizontal
        win = all(self.fields[i][x].marked for i in range(self.size))
        #
        win |= all(field.marked for field in self.fields[y])
        return win

    def score(self, value: int):
        score = 0
        self.print()
        for row in self.fields:
            for field in row:
                if not field.marked:
                    score += field.value
        return score * value

    def print(self):
        import pprint
        pprint.pprint(self.value_to_position)
        for row in self.fields:
            for field in row:
                print(f"({field.value}, {field.marked}) ", end='')
            print()


def load_data():
    with open('day4_input.txt') as infile:
        data = infile.read()
    lines = data.splitlines()
    values = map(int, lines[0].split(','))
    boards = []
    board_size = len(lines[2].split())
    for i in range(2, len(lines), board_size+1):
        boards.append(Board(lines[i:i+board_size]))
    return boards, values


def p1():
    boards, values = load_data()

    for value in values:
        for board in boards:
            if board.mark(value):
                return board.score(value)


def p2():
    boards, values = load_data()

    for value in values:
        next_stage = []
        for board in boards:
            if not board.mark(value):
                next_stage.append(board)
        if len(next_stage) == 0:
            return board.score(value)
        boards = next_stage


if __name__ == "__main__":
    print('Part 1 Score: ', p1())
    print('Part 2 score: ', p2())
