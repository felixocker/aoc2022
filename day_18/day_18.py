#!/usr/bin/env python3
"""AOC 2022 day 18"""


import numpy as np
from aocd.models import Puzzle


def parse(data):
    return [[int(i) for i in d.split(",")] for d in data.strip().split("\n")]


class Droplet:
    def __init__(self, cube_data) -> None:
        self.lnx = max(c[0] for c in cube_data) + 1
        self.lny = max(c[1] for c in cube_data) + 1
        self.lnz = max(c[2] for c in cube_data) + 1
        self.mtrx: np.array = np.zeros((self.lnx, self.lny, self.lnz))
        for cube in cube_data:
            self.mtrx[cube[0]][cube[1]][cube[2]] = 1
        self.padded = np.pad(self.mtrx, pad_width=1, constant_values=np.nan)

    def count_neighbours(self, point: tuple) -> int:
        dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        neighbour_count = 0
        for d in dirs:
            if self.padded[point[0] + d[0]][point[1] + d[1]][point[2] + d[2]] == 1:
                neighbour_count += 1
        return neighbour_count

    def remove_enclaves(self):
        """set value of enclaves to 1"""
        dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        queue = [(1, 1, 1)]
        while queue:
            point = queue.pop()
            self.padded[point[0]][point[1]][point[2]] = 2
            for d in dirs:
                neighbour = (point[0] + d[0], point[1] + d[1], point[2] + d[2])
                if self.padded[neighbour] == np.nan:
                    continue
                if self.padded[neighbour[0]][neighbour[1]][neighbour[2]] == 0:
                    queue.append(neighbour)
        for x in range(1, self.lnx+1):
            for y in range(1, self.lny+1):
                for z in range(1, self.lnz+1):
                    if self.padded[x][y][z] == 0:
                        self.padded[x][y][z] = 1
                    elif self.padded[x][y][z] == 2:
                        self.padded[x][y][z] = 0

    def calc_surface(self):
        surface = 0
        for x in range(1, self.lnx+1):
            for y in range(1, self.lny+1):
                for z in range(1, self.lnz+1):
                    if self.padded[x][y][z] == 1:
                        surface += 6 - self.count_neighbours((x, y, z))
        return surface


def part_a(data):
    droplet = Droplet(parse(data))
    return droplet.calc_surface()


def part_b(data):
    droplet = Droplet(parse(data))
    droplet.remove_enclaves()
    return droplet.calc_surface()


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=18)
    test = """2,2,2\n1,2,2\n3,2,2\n2,1,2\n2,3,2\n2,2,1\n2,2,3\n2,2,4\n2,2,6\n1,2,5\n3,2,5\n2,1,5\n2,3,5\n"""

    print("Part A")
    assert part_a(test) == 64
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 58
    print(part_b(puzzle.input_data))
