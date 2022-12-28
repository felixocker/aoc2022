#!/usr/bin/env python3
"""
AOC 2022 day 23
"""


from collections import Counter

from aocd.models import Puzzle


def parse(data: str) -> list:
    return [[i for i in l] for l in data.strip().split("\n")]


class Swarm:

    collision_fields = {
        (-1, 0): ((-1, 0), (-1, -1), (-1, 1)),
        (1, 0): ((1, 0), (1, -1), (1, 1)),
        (0, -1): ((0, -1), (-1, -1), (1, -1)),
        (0, 1): ((0, 1), (-1, 1), (1, 1)),
    }

    def __init__(self, data: list, height: int, width: int) -> None:
        self.dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.dimensions = (height, width)
        self.elves = set()
        self.suggestions = dict()
        for x, vx in enumerate(data):
            for y, vy in enumerate(vx):
                if vy == "#":
                    self.elves.add((x, y))

    def check(self) -> None:
        self.suggestions = dict()
        for elf in self.elves:
            adjacent = [(elf[0]+x, elf[1]+y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x != 0 or y != 0]
            if not any(d in self.elves for d in adjacent):
                continue
            for i in range(4):
                d = self.dirs[i]
                cf = [(elf[0] + t[0], elf[1] + t[1]) for t in self.collision_fields[d]]
                if not any(p in self.elves for p in cf):
                    self.suggestions[elf] = (elf[0] + d[0], elf[1] + d[1])
                    break
        self.dirs.append(self.dirs.pop(0))

    def check_equilibrium(self) -> bool:
        return not self.suggestions

    def move(self) -> None:
        counter = Counter(self.suggestions.values())
        for elf in self.suggestions:
            if counter[self.suggestions[elf]] == 1:
                self.elves.remove(elf)
                self.elves.add(self.suggestions[elf])

    def layout(self, padding: int) -> None:
        """print the entire swarm of elves
        :param padding: number of moves - indicates maximum movement to the outside
        """
        field = [["."] * (self.dimensions[1] + 2*padding) for _ in range(self.dimensions[0] + 2*padding)]
        for e in self.elves:
            field[e[0] + padding][e[1] + padding] = "#"
        print(*["".join(r) for r in field], sep="\n")

    def calc_empty_ground(self) -> int:
        height = max(e[0] for e in self.elves) - min(e[0] for e in self.elves)
        width = max(e[1] for e in self.elves) - min(e[1] for e in self.elves)
        return (height + 1) * (width + 1) - len(self.elves)


def part_a(data: str, rounds: int = 10) -> int:
    swarm_data = parse(data)
    swarm = Swarm(swarm_data, height=len(swarm_data), width=len(swarm_data[0]))
    for _ in range(rounds):
        swarm.check()
        swarm.move()
        # swarm.layout(rounds)
    return swarm.calc_empty_ground()


def part_b(data: str) -> int:
    swarm_data = parse(data)
    swarm = Swarm(swarm_data, height=len(swarm_data), width=len(swarm_data[0]))
    cnt = 0
    while True:
        cnt += 1
        swarm.check()
        if swarm.check_equilibrium():
            return cnt
        swarm.move()


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=23)
    test = (
        """....#..\n"""
        """..###.#\n"""
        """#...#.#\n"""
        """.#...##\n"""
        """#.###..\n"""
        """##.#.##\n"""
        """.#..#..\n"""
    )

    print("Part A")
    assert part_a(test) == 110
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 20
    print(part_b(puzzle.input_data))
