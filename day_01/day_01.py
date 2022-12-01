#!/usr/bin/env python3
"""AOC 2022 day 1"""


from aocd.models import Puzzle


def part_a(data) -> int:
    inventory = [sum([int(m) for m in i.split("\n")]) for i in data.split("\n\n")]
    return max(inventory)


def part_b(data, num_elves: int = 3) -> int:
    inventory = [sum([int(m) for m in i.split("\n")]) for i in data.split("\n\n")]
    maxcal = inventory[:num_elves]
    maxcal.sort(reverse=True)
    for i in inventory[num_elves:]:
        if i > maxcal[-1]:
            maxcal.pop()
            maxcal.append(i)
            maxcal.sort(reverse=True)
    return sum(maxcal)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=1)
    print("Part A")
    print(part_a(puzzle.input_data))
    print("Part B")
    print(part_b(puzzle.input_data, 3))
