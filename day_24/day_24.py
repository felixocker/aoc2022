#!/usr/bin/env python3
"""
AOC 2022 day 24
"""


from aocd.models import Puzzle


def parse(data: str) -> list:
    return [[f for f in l] for l in data.strip().split("\n")]


class ValleySim:

    blizzard_directions = {
        ">": (0, 1),
        "<": (0, -1),
        "^": (-1, 0),
        "v": (1, 0),
    }
    moves = ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))

    def __init__(self, data: list) -> None:
        self.field = data
        self.dimensions = (len(data), len(data[0]))
        self.blizzards = {}
        for ci, vi in enumerate(self.field):
            for cj, vj in enumerate(vi):
                if vj not in (".", "#"):
                    self.blizzards[(ci, cj)] = self.blizzard_directions[vj]
                    self.field[ci][cj] = "."
        self.start = (0, self.field[0].index("."))
        self.end = (self.dimensions[0] - 1, self.field[-1].index("."))
        self.steps = 0
        self.positions = {self.start}

    def move(self, pos: tuple) -> tuple:
        x, y = pos
        for m in self.moves:
            if 0 <= x + m[0] < self.dimensions[0]:
                if self.field[x + m[0]][y + m[1]] != "#":
                    yield x + m[0], y + m[1]

    def move_bliz(self, pos: tuple) -> tuple:
        x, y = pos
        dx, dy = self.blizzards[pos]
        xx = (x + self.steps * dx - 1) % (self.dimensions[0] - 2) + 1
        yy = (y + self.steps * dy - 1) % (self.dimensions[1] - 2) + 1
        return xx, yy

    def run(self, goal: tuple) -> int:
        self.steps += 1
        nxt = set()
        for p in self.positions:
            nxt.update(set(self.move(p)))
        blizzards = set()
        for b in self.blizzards:
            bliz = self.move_bliz(b)
            blizzards.add(bliz)
        nxt -= blizzards
        if not nxt:
            raise Exception("Reaching the goal is impossible")
        if goal in nxt:
            return self.steps
        self.positions = nxt
        return self.run(goal)

    def get_snacks(self) -> int:
        self.run(self.end)
        self.positions = {self.end}
        self.run(self.start)
        self.positions = {self.start}
        return self.run(self.end)


def part_a(data: str) -> int:
    valley_data = parse(data)
    valley_sim = ValleySim(valley_data)
    return valley_sim.run(valley_sim.end)


def part_b(data: str) -> int:
    valley_data = parse(data)
    valley_sim = ValleySim(valley_data)
    return valley_sim.get_snacks()


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=24)
    test = (
        """#.######\n"""
        """#>>.<^<#\n"""
        """#.<..<<#\n"""
        """#>v.><>#\n"""
        """#<^v^^>#\n"""
        """######.#\n"""
    )

    print("Part A")
    assert part_a(test) == 18
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 54
    print(part_b(puzzle.input_data))
