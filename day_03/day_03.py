#!/usr/bin/env python3
"""AOC 2022 day 3"""


import string

from aocd.models import Puzzle


def part_a(data):
    priorities = {v: c+1 for c, v in enumerate(string.ascii_letters)}
    rucksacks = [(i[:len(i)//2], i[len(i)//2:]) for i in data.split("\n")]
    prio_sum = 0
    for r in rucksacks:
        prio_sum += priorities[list(set(r[0]) & set(r[1]))[0]]
    return prio_sum


def part_b(data):
    priorities = {v: c + 1 for c, v in enumerate(string.ascii_letters)}
    rucksacks = [i for i in data.split("\n")]
    prio_sum = 0
    while rucksacks:
        e1, e2, e3 = rucksacks[:3]
        rucksacks = rucksacks[3:]
        prio_sum += priorities[list(set(e1) & set(e2) & set(e3))[0]]
    return prio_sum


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=3)
    print("Part A")
    print(part_a(puzzle.input_data))
    print("Part B")
    print(part_b(puzzle.input_data))
