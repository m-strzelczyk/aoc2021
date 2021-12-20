# https://adventofcode.com/2021/day/18
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import math
import copy


class Explosion(Exception):
    def __init__(self, left, right):
        self.left = left
        self.right = right

@dataclass
class Node:
    left: Optional[Node]
    right: Optional[Node]
    value: Optional[int]

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return f"[{self.left},{self.right}]"

    def add_value(self, left: bool, value: int):
        if value is None:
            return
        if self.value is not None:
            self.value += value
        else:
            if left:
                self.left.add_value(True, value)
            else:
                self.right.add_value(False, value)

    def explode(self, depth=0):
        if self.value is not None:
            return
        if depth == 4:
            self.value = 0
            exp = Explosion(self.left.value, self.right.value)
            # print(f"Pair {self.left} {self.right} goes boom!")
            self.left = None
            self.right = None
            return exp
        else:
            # print(f"Processing {self}, depth {depth}")
            boom = self.left.explode(depth+1)
            if boom is not None:
                self.right.add_value(True, boom.right)
                boom.right = None
                return boom
            boom = self.right.explode(depth+1)
            if boom is not None:
                self.left.add_value(False, boom.left)
                boom.left = None
                return boom
        return None

    def split(self):
        if self.value is not None and self.value >= 10:
            # print(f"Splitting {self.value}")
            self.left = Node(value=math.floor(self.value / 2), right=None, left=None)
            self.right = Node(value=math.ceil(self.value / 2), right=None, left=None)
            self.value = None
            return True
        elif self.value is not None:
            return False
        else:
            return self.left.split() or self.right.split()

    def add_node(self, node: Node):
        return Node(left=self, right=node, value=None)

    def magnitude(self):
        if self.value is not None:
            return self.value
        else:
            return 3*self.left.magnitude() + 2*self.right.magnitude()


def build_tree(inpt: str) -> (Node, str):
    if inpt[0] != '[':
        assert(inpt[0].isdigit())
        return Node(left=None, right=None, value=int(inpt[0])), inpt[1:]
    assert(inpt[0] == '[')
    left, inpt = build_tree(inpt[1:])
    assert(inpt[0] == ',')
    right, inpt = build_tree(inpt[1:])
    assert(inpt[0] == ']')
    return Node(left=left, right=right, value=None), inpt[1:]


def keep_reducing(tree: Node):
    while True:
        # print(tree)
        exp = tree.explode(0)
        if exp is not None:
            continue
        split = tree.split()
        if split:
            continue
        break


def p1(inpt: str) -> int:
    trees = []
    for line in inpt.splitlines():
        trees.append(build_tree(line)[0])
    tree = trees[0]
    for next_tree in trees[1:]:
        tree = tree.add_node(next_tree)
        keep_reducing(tree)
    return tree.magnitude()


def p2(inpt: str) -> int:
    trees = []
    for line in inpt.splitlines():
        trees.append(build_tree(line)[0])
    tree_pairs = [(t1, t2) for t1 in trees for t2 in trees]
    max_mag = 0
    for i, (tree1, tree2) in enumerate(tree_pairs):
        if tree1 == tree2:
            continue
        t = copy.deepcopy(tree1.add_node(tree2))
        keep_reducing(t)
        max_mag = max(max_mag, t.magnitude())
    return max_mag


if __name__ == '__main__':
    with open('input.txt') as infile:
        data = infile.read()
    print("P1:", p1(data))
    print("P2:", p2(data))
