#!/usr/bin/env python3
"""AOC 2022 day 13"""


import json
from functools import cmp_to_key

from aocd.models import Puzzle


def parse(data) -> list:
    return [[json.loads(e) for e in p.strip().split("\n")] for p in data.strip().split("\n\n")]


def compare_lists(left: list, right: list):
    if left and right:
        cmp = compare(left[0], right[0])
        if cmp != 0:
            return cmp
        else:
            return compare(left[1:], right[1:])
    return compare(len(left), len(right))


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    return compare_lists(left if isinstance(left, list) else [left], right if isinstance(right, list) else [right])


def part_a(data: str) -> int:
    return sum(c for c, v in enumerate(parse(data), 1) if compare(*v) < 0)


def part_b(data: str) -> int:
    packets = parse(data)
    dividers = [[[2]], [[6]]]
    packets.append(dividers)
    flat = [elem for pair in packets for elem in pair]
    srtd = sorted(flat, key=cmp_to_key(compare))
    return (srtd.index(dividers[0]) + 1) * (srtd.index(dividers[1]) + 1)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=13)
    test = (
        """[1,1,3,1,1]\n[1,1,5,1,1]\n\n[[1],[2,3,4]]\n[[1],4]\n\n"""
        """[9]\n[[8,7,6]]\n\n[[4,4],4,4]\n[[4,4],4,4,4]\n\n"""
        """[7,7,7,7]\n[7,7,7]\n\n[]\n[3]\n\n"""
        """[[[]]]\n[[]]\n\n[1,[2,[3,[4,[5,6,7]]]],8,9]\n[1,[2,[3,[4,[5,6,0]]]],8,9]\n"""
    )

    print("Part A")
    assert part_a(test) == 13
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 140
    print(part_b(puzzle.input_data))
