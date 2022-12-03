#!/usr/bin/env python3
"""AOC 2022 day 3"""


import string

from aocd.models import Puzzle


def first_common_elem(stra: str, strb: str) -> str:
    for a in set(stra):
        for b in set(strb):
            if a == b:
                return a


def part_a(data):
    priorities = {v: c+1 for c, v in enumerate(string.ascii_letters)}
    rucksacks = [(i[:len(i)//2], i[len(i)//2:]) for i in data.split("\n")]
    prio_sum = 0
    for r in rucksacks:
        prio_sum += priorities[first_common_elem(r[0], r[1])]
    return prio_sum


def part_b(data):
    priorities = {v: c + 1 for c, v in enumerate(string.ascii_letters)}
    rucksacks = [i for i in data.split("\n")]
    prio_sum = 0
    for i in range(len(rucksacks) // 3):
        e1, e2, e3 = rucksacks[i*3:i*3+3]
        prio_sum += priorities[first_common_elem("".join(set(e1) & set(e2)), e3)]
    return prio_sum


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=3)
    print("Part A")
    print(part_a(puzzle.input_data))
    print("Part B")
    print(part_b(puzzle.input_data))
