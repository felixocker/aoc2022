#!/usr/bin/env python3
"""AOC 2022 day 6"""


from aocd.models import Puzzle


def both(data, ln: int) -> int:
    pos, mem = ln, list(data[:ln])
    for char in data[ln:]:
        if len(set(mem)) == ln:
            return pos
        mem.pop(0)
        mem.append(char)
        pos += 1


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=6)
    print("Part A")
    print(both(puzzle.input_data, ln=4))
    print("Part B")
    print(both(puzzle.input_data, ln=14))
