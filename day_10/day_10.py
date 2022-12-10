#!/usr/bin/env python3
"""AOC 2022 day 10"""


import pandas as pd
from aocd.models import Puzzle


def parse(data) -> list:
    return [l.split() for l in data.split("\n") if l]


def part_a(data):
    register, cycle = 1, 0
    signal_sum = 0

    def _check_signal_strength(cycle: int, register: int) -> int:
        if cycle == 20 or (cycle - 20) % 40 == 0:
            return cycle * register
        return 0

    for instruction in parse(data):
        if cycle > 220:
            break
        if instruction[0] == "noop":
            cycle += 1
            signal_sum += _check_signal_strength(cycle, register)
        else:
            for _ in range(2):
                cycle += 1
                signal_sum += _check_signal_strength(cycle, register)
            register += int(instruction[1])

    return signal_sum


def part_b(data, rows: int = 6, columns: int = 40) -> None:
    image = pd.DataFrame(".", index=range(rows), columns=range(columns))
    register, cycle = 1, 0

    def _draw(cycle: int, register: int) -> None:
        c, r = (cycle-1) % 40, (cycle-1) // 40
        if register-1 <= c <= register+1:
            image[c][r] = "#"

    for instruction in parse(data):
        if cycle > rows * columns:
            break
        if instruction[0] == "noop":
            cycle += 1
            _draw(cycle, register)
        else:
            for _ in range(2):
                cycle += 1
                _draw(cycle, register)
            register += int(instruction[1])

    print(image)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=10)
    with open("test.txt") as f:
        test = f.read()

    print("Part A")
    assert part_a(test) == 13140
    print(part_a(puzzle.input_data))

    print("Part B")
    print("NOTE: take a step back to see the pattern more clearly")
    print("Image for test case:")
    part_b(test)
    print("Puzzle result:")
    part_b(puzzle.input_data)
