#!/usr/bin/env python3
"""AOC 2022 day 5"""


from aocd.models import Puzzle


def load_data(data) -> tuple:
    stack_data, moves_data = data.split("\n\n")
    # init stacks
    stack_data = stack_data.split("\n")
    stacks = {k: [] for k in range(1, len(stack_data[-1].split())+1)}
    for row in stack_data[-2::-1]:
        for k in stacks.keys():
            crate = row[1 + 4 * (k-1)]
            if crate != " ":
                stacks[k].append(crate)
    # split moves
    moves_data = moves_data.split("\n")
    moves = [[int(v) for c, v in enumerate(m.split()) if c % 2 == 1] for m in moves_data]
    return stacks, moves


def part_a(data):
    stacks, moves = load_data(data)

    def _move(source: int, sink: int) -> None:
        stacks[sink].append(stacks[source].pop())

    for m in moves:
        for _ in range(m[0]):
            _move(m[1], m[2])

    return "".join([stacks[k][-1] for k in stacks.keys() if stacks[k]])


def part_b(data):
    stacks, moves = load_data(data)

    def _move(source: int, sink: int, amount: int) -> None:
        stacks[sink].extend(stacks[source][-amount:])
        for _ in range(amount):
            stacks[source].pop()

    for m in moves:
        _move(m[1], m[2], m[0])

    return "".join([stacks[k][-1] for k in stacks.keys() if stacks[k]])


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=5)
    print("Part A")
    print(part_a(puzzle.input_data))
    print("Part B")
    print(part_b(puzzle.input_data))
