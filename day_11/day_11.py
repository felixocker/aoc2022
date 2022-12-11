#!/usr/bin/env python3
"""AOC 2022 day 11"""


from __future__ import annotations

import math

from aocd.models import Puzzle


def parse(data) -> list:
    monkey_data = [m for m in data.split("\n\n")]
    monkeys = []
    for m in monkey_data:
        md = m.split("\n")
        monkey = {
            "monkey_id": int(md[0][:-1].split()[-1]),
            "items": [int(i) for i in md[1].split(": ")[-1].split(", ")],
            "operation_type": md[2].split(" = ")[-1].split()[1],
            "operation_value": md[2].split(" = ")[-1].split()[2],
            "test_value": int(md[3].split()[-1]),
            "true_monkey": int(md[4].split()[-1]),
            "false_monkey": int(md[5].split()[-1]),
        }
        monkeys.append(monkey)
    return monkeys


class Item:

    def __init__(self, item_id: int) -> None:
        self.item_id = item_id
        self.worry_level = item_id


class Monkey:

    def __init__(self, monkey_id: int, items: list[int], operation_type: str,
                 operation_value: str, test_value: int
                 ) -> None:
        self.monkey_id = monkey_id
        self.items = [Item(i) for i in items]
        self.operation_type = operation_type
        self.operation_value = operation_value
        self.test_value = test_value
        self.true_monkey = None
        self.false_monkey = None
        self.inspection_count = 0

    def set_monkeys(self, true_monkey: Monkey, false_monkey: Monkey) -> None:
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey

    def receive(self, item) -> None:
        self.items.append(item)

    def run(self, supermod: int = None):
        while self.items:
            item = self.items.pop(0)
            self._inspect(item)
            if supermod is None:
                item.worry_level //= 3
            else:
                item.worry_level %= supermod
            if item.worry_level % self.test_value == 0:
                self.true_monkey.receive(item)
            else:
                self.false_monkey.receive(item)

    def _inspect(self, item: Item) -> None:
        self.inspection_count += 1
        if self.operation_value == "old":
            val = item.worry_level
        else:
            val = int(self.operation_value)
        match self.operation_type:
            case "*":
                item.worry_level *= val
            case "+":
                item.worry_level += val
            case _:
                raise Exception("invalid operation_type for monkey test")


def monkey_init(data) -> list:
    monkey_data = parse(data)
    monkeys = []
    for m in monkey_data:
        monkeys.append(Monkey(*list(m.values())[:-2]))
    for c, m in enumerate(monkey_data):
        monkeys[c].set_monkeys(monkeys[m["true_monkey"]], monkeys[m["false_monkey"]])
    return monkeys


def part_a(data, rounds: int = 20):
    monkeys = monkey_init(data)
    for _ in range(rounds):
        for m in monkeys:
            m.run()
    inspections = sorted([m.inspection_count for m in monkeys], reverse=True)
    return inspections[0] * inspections[1]


def part_b(data, rounds: int = 10000):
    monkeys = monkey_init(data)
    supermod = math.prod(m.test_value for m in monkeys)
    for _ in range(rounds):
        for m in monkeys:
            m.run(supermod=supermod)
    inspections = sorted([m.inspection_count for m in monkeys], reverse=True)
    return inspections[0] * inspections[1]


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=11)
    with open("test.txt") as f:
        test = f.read()

    print("Part A")
    assert part_a(test) == 10605
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 2713310158
    print(part_b(puzzle.input_data))
