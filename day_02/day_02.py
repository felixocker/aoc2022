#!/usr/bin/env python3
"""AOC 2022 day 2"""


from aocd.models import Puzzle


def part_a(data) -> int:
    points = 0
    for r in [i.split() for i in data.split("\n")]:
        opp = "ABC".index(r[0])
        me = "XYZ".index(r[1])
        res = (me - opp + 1) % 3
        points += 3 * res + me + 1
    return points


def part_b(data) -> int:
    points = 0
    for r in [i.split() for i in data.split("\n")]:
        opp = "ABC".index(r[0])
        res = "XYZ".index(r[1])
        me = (opp + res - 1) % 3
        points += 3 * res + me + 1
    return points


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=2)
    print("Part A")
    print(part_a(puzzle.input_data))
    print("Part B")
    print(part_b(puzzle.input_data))
