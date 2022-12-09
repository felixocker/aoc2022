#!/usr/bin/env python3
"""AOC 2022 day 9"""


from aocd.models import Puzzle


def parse(data):
    return [[i.split()[0], int(i.split()[1])] for i in data.split("\n") if i]


def move(coords: tuple, direction: str) -> tuple:
    moves = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }
    return coords[0]+moves[direction][0], coords[1]+moves[direction][1]


def follow(pos1: tuple, pos2: tuple) -> tuple:
    if abs(pos1[0]-pos2[0]) <= 1 and abs(pos1[1]-pos2[1]) <= 1:
        return pos2
    if pos1[0] == pos2[0]:
        x = pos1[0]
    elif abs(pos1[0] - pos2[0]) == 1:
        x = pos1[0]
    else:
        x = (pos1[0] + pos2[0]) // 2
    if pos1[1] == pos2[1]:
        y = pos1[1]
    elif abs(pos1[1]-pos2[1]) <= 1:
        y = pos1[1]
    else:
        y = (pos1[1] + pos2[1]) // 2
    return x, y


def part_a(data) -> int:
    moves = parse(data)
    head, tail = (0, 0), (0, 0)
    visited = {tail}
    for m in moves:
        for _ in range(m[1]):
            head = move(head, m[0])
            tail = follow(head, tail)
            visited.add(tail)
    return len(visited)


def part_b(data) -> int:
    moves = parse(data)
    rope = [(0, 0) for _ in range(10)]
    visited = {rope[-1]}
    for m in moves:
        for _ in range(m[1]):
            rope[0] = move(rope[0], m[0])
            for i in range(1, 10):
                rope[i] = follow(rope[i-1], rope[i])
            visited.add(rope[-1])
    return len(visited)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=9)
    with open("test.txt") as f:
        test = f.read()

    print("Part A")
    assert part_a(test) == 13
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 1
    test_2 = """R 5\nU 8\nL 8\nD 3\nR 17\nD 10\nL 25\nU 20\n"""
    assert part_b(test_2) == 36
    print(part_b(puzzle.input_data))
