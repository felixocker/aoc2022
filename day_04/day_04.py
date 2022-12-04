#!/usr/bin/env python3
"""AOC 2022 day 4"""


from aocd.models import Puzzle


def both(data) -> tuple:
    assignments = [i.split(",") for i in data.split("\n")]
    subsumptions, overlaps = 0, 0
    for a in assignments:
        l1, u1 = a[0].split("-")
        l2, u2 = a[1].split("-")
        if int(l1) <= int(l2) and int(u1) >= int(u2) or int(l1) >= int(l2) and int(u1) <= int(u2):
            subsumptions += 1
        if int(l2) <= int(l1) <= int(u2) or int(l2) <= int(u1) <= int(u2) or \
                int(l1) <= int(l2) <= int(u1) or int(l1) <= int(u2) <= int(u1):
            overlaps += 1
    return subsumptions, overlaps


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=4)
    solution_a, solution_b = both(puzzle.input_data)
    print("Part A")
    print(solution_a)
    print("Part B")
    print(solution_b)
