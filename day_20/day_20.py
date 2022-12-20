#!/usr/bin/env python3
"""AOC 2022 day 20"""


from aocd.models import Puzzle


def parse(data) -> list:
    return [int(v) for v in data.strip().split("\n")]


class File:
    def __init__(self, data: list) -> None:
        self.values = data
        self.ln = len(data)
        self.indices = list(range(self.ln))

    def mix(self, reps: int = 1) -> None:
        for _ in range(reps):
            for num_id in range(self.ln):
                pos = self.indices.index(num_id)
                self.indices.pop(pos)
                self.indices.insert((pos + self.values[num_id]) % (self.ln - 1), num_id)

    def find_start(self) -> int:
        return self.indices.index(self.values.index(0))

    def apply_decryption_key(self, key: int) -> None:
        for c, _ in enumerate(self.values):
            self.values[c] *= key

    def nth_elem(self, start: int, offset: int) -> int:
        return self.values[self.indices[(start + offset) % self.ln]]

    def grove_coordinates(self) -> int:
        start = self.find_start()
        res = 0
        for i in 1000, 2000, 3000:
            res += self.nth_elem(start, i)
        return res


def part_a(data) -> int:
    f = File(parse(data))
    f.mix()
    return f.grove_coordinates()


def part_b(data) -> int:
    f = File(parse(data))
    f.apply_decryption_key(811589153)
    f.mix(10)
    return f.grove_coordinates()


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=20)
    test = """1\n2\n-3\n3\n-2\n0\n4\n"""

    print("Part A")
    assert part_a(test) == 3
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 1623178306
    print(part_b(puzzle.input_data))
