#!/usr/bin/env python3
"""AOC 2022 day 8"""


import numpy as np
from aocd.models import Puzzle


def parse(data) -> np.ndarray:
    grid = np.asarray([[int(i) for i in row] for row in data.split("\n") if row])
    return np.pad(array=grid, pad_width=1, mode='constant', constant_values=-1)


def part_a(data) -> int:
    grid = parse(data)
    trees_quantity = (grid.shape[0]-2) * (grid.shape[1]-2)

    def _iterate(lst: list, start: int, move_dir: int) -> list:
        invisible = []
        highest = lst[start]
        i = start + move_dir * 1
        while lst[i] != -1:
            if lst[i] <= highest:
                invisible.append(i)
            else:
                highest = lst[i]
            i += move_dir * 1
        return invisible

    def _check_visibility_rows(start: int, move_dir: int) -> set:
        invisible = set()
        for x in range(1, grid.shape[0]-1):
            row = grid[x, :]
            for y in _iterate(row, start, move_dir):
                invisible.add((x, y))
        return invisible

    def _check_visibility_columns(start: int, move_dir: int) -> set:
        invisible = set()
        for y in range(1, grid.shape[1]-1):
            col = grid[:, y]
            for x in _iterate(col, start, move_dir):
                invisible.add((x, y))
        return invisible

    from_left = _check_visibility_rows(1, 1)
    from_right = _check_visibility_rows(grid.shape[0]-2, -1)
    from_top = _check_visibility_columns(1, 1)
    from_bottom = _check_visibility_columns(grid.shape[1]-2, -1)

    return trees_quantity - len(set.intersection(from_left, from_right, from_top, from_bottom))


def part_b(data):
    grid = parse(data)
    max_score = 0
    for x in range(1, grid.shape[0]-1):
        for y in range(1, grid.shape[1]-1):
            score = 1
            for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x+direction[0], y+direction[1]
                dir_score = 0
                while grid[nx][ny] != -1:
                    dir_score += 1
                    if grid[x][y] <= grid[nx][ny]:
                        break
                    nx += direction[0]
                    ny += direction[1]
                score *= dir_score
                if dir_score == 0:
                    break
            max_score = max(max_score, score)
    return max_score


if __name__ == "__main__":
    with open("test.txt") as f:
        test = f.read()
    puzzle = Puzzle(year=2022, day=8)

    print("Part A")
    test_res = part_a(test)
    assert test_res == 21, f"{test_res} is the wrong result for test"
    print(part_a(puzzle.input_data))

    print("Part B")
    test_res = part_b(test)
    assert test_res == 8, f"{test_res} is the wrong result for test"
    print(part_b(puzzle.input_data))
