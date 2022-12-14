#!/usr/bin/env python3
"""AOC 2022 day 14"""


import pandas as pd
from aocd.models import Puzzle


def create_map(data, wide: bool = False) -> tuple[pd.DataFrame, tuple, int, int]:
    rock_data = [[[int(e) for e in r.split(",")] for r in l.split(" -> ")] for l in data.strip().split("\n")]
    height = max(r[1] for p in rock_data for r in p)
    if not wide:
        left = min(r[0] for p in rock_data for r in p)
        right = max(r[0] for p in rock_data for r in p)
        cave = pd.DataFrame(".", index=range(height+1), columns=range(right-left+1))
    else:
        left = min(min(r[0] for p in rock_data for r in p), 500-height-2)
        right = max(max(r[0] for p in rock_data for r in p), 500+height+2)
        cave = pd.DataFrame(".", index=range(height + 1), columns=range(right - left + 1))
    for path in rock_data:
        for c, rock in enumerate(path):
            if c == 0:
                cave[rock[0]-left][rock[1]] = "#"
                continue
            # vertical path
            if rock[0] == path[c-1][0]:
                for x in range(min(rock[1], path[c-1][1]), max(rock[1], path[c-1][1])):
                    cave[rock[0]-left][x] = "#"
            # horizontal path
            if rock[1] == path[c-1][1]:
                for x in range(min(rock[0], path[c-1][0]), max(rock[0], path[c-1][0])+1):
                    cave[x-left][rock[1]] = "#"
    cave[500-left][0] = "+"
    return cave, (500-left, 0), right-left, height


class SandUnit:

    def __init__(self, start: tuple):
        self.pos = list(start)

    def move(self, cave: pd.DataFrame, width: int, height: int) -> bool:
        in_field = True
        while True:
            x, y = self.pos
            if cave[x][y] == "o" or y == height:
                in_field = False
                break
            elif cave[x][y+1] == ".":
                self.pos = [x, y+1]
            elif x == 0:
                in_field = False
                break
            elif cave[x-1][y+1] == ".":
                self.pos = [x-1, y+1]
            elif x == width:
                in_field = False
                break
            elif cave[x+1][y+1] == ".":
                self.pos = [x+1, y+1]
            else:
                cave[x][y] = "o"
                break
        return in_field


def pile_up(cave, start, width, height):
    cnt = -1
    while True:
        cnt += 1
        su = SandUnit(start)
        if not su.move(cave, width, height):
            break
    return cnt


def part_a(data) -> int:
    return pile_up(*create_map(data))


def extend_map(data) -> tuple[pd.DataFrame, tuple, int, int]:
    cave, start, width, height = create_map(data, wide=True)
    cave.loc[len(cave)] = ["." for _ in range(width+1)]
    cave.loc[len(cave)] = ["#" for _ in range(width+1)]
    height += 2
    return cave, start, width, height


def part_b(data) -> int:
    return pile_up(*extend_map(data))


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=14)
    test = """498,4 -> 498,6 -> 496,6\n503,4 -> 502,4 -> 502,9 -> 494,9\n"""

    print("Part A")
    assert part_a(test) == 24
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 93
    print(part_b(puzzle.input_data))
