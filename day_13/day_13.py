#!/usr/bin/env python3
"""AOC 2022 day 13"""


import json
from itertools import zip_longest

from aocd.models import Puzzle


def parse(data) -> list:
    return [[json.loads(e) for e in p.strip().split("\n")] for p in data.strip().split("\n\n")]


def preprocess(pair: list) -> list:
    packet1, packet2 = pair
    tp1, tp2 = type(packet1), type(packet2)
    if packet1 is None or packet2 is None:
        return [packet1, packet2]
    if tp1 == int and tp2 == int:
        return [packet1, packet2]
    if tp1 == int:
        return preprocess([[packet1], packet2])
    if tp2 == int:
        return preprocess([packet1, [packet2]])
    if tp1 == list and tp2 == list:
        p1, p2 = [], []
        for sub_pair in zip_longest(packet1, packet2):
            r1, r2 = preprocess(list(sub_pair))
            if r1 is not None:
                p1.append(r1)
            if r2 is not None:
                p2.append(r2)
        return [p1, p2]


def part_a(data):
    packets = parse(data)
    res = []
    for c, pair in enumerate(packets):
        left, right = preprocess(pair)
        if left < right:
            res.append(c+1)
    return sum(res)


def part_b(data):
    packets = parse(data)
    dividers = [[[2]], [[6]]]
    packets.append(dividers)
    flat = [packet for pair in packets for packet in pair]
    for _ in range(ln := len(flat)-1):
        for c in range(ln):
            first, second = preprocess([flat[c], flat[c+1]])
            if first >= second:
                flat[c], flat[c+1] = flat[c+1], flat[c]
    return (flat.index(dividers[0]) + 1) * (flat.index(dividers[1]) + 1)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=13)
    test = """[1,1,3,1,1]\n[1,1,5,1,1]\n\n[[1],[2,3,4]]\n[[1],4]\n\n[9]\n[[8,7,6]]\n\n[[4,4],4,4]\n[[4,4],4,4,4]\n\n
        [7,7,7,7]\n[7,7,7]\n\n[]\n[3]\n\n[[[]]]\n[[]]\n\n[1,[2,[3,[4,[5,6,7]]]],8,9]\n[1,[2,[3,[4,[5,6,0]]]],8,9]\n"""

    print("Part A")
    assert part_a(test) == 13
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 140
    print(part_b(puzzle.input_data))
