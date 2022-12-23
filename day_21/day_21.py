#!/usr/bin/env python3
"""AOC 2022 day 21"""


from abc import ABC
from abc import abstractmethod

from aocd.models import Puzzle


def parse(data) -> tuple[list, list]:
    numbers, operations = [], []
    for l in data.strip().split("\n"):
        i = l.split(" ")
        if len(i) == 2:
            numbers.append((i[0][:-1], int(i[1])))
        else:
            operations.append((i[0][:-1], i[1], i[2], i[3]))
    return numbers, operations


class MathMonkey(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.value = None

    @abstractmethod
    def return_val(self):
        return NotImplemented


class NumberMonkey(MathMonkey):
    def __init__(self, number: int, name: str) -> None:
        super().__init__(name)
        self.value = number

    def return_val(self) -> int:
        return self.value


class OperationMonkey(MathMonkey):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.first = None
        self.second = None
        self.operator = None

    def set_info(self, first: MathMonkey, second: MathMonkey, operator: str) -> None:
        self.first = first
        self.second = second
        self.operator = operator

    def return_val(self) -> int:
        first = self.first.return_val()
        second = self.second.return_val()
        assert self.operator in ("+", "-", "*", "/")
        assert isinstance(first, int)
        assert isinstance(second, int)
        return int(eval(str(first) + self.operator + str(second)))


def init_monkeys(nums: list, ops: list) -> dict:
    monkeys = dict()
    for n in nums:
        name, number = n
        monkeys[name] = NumberMonkey(number, name)
    for o in ops:
        name, first, operator, second = o
        if first not in monkeys:
            monkeys[first] = OperationMonkey(first)
        fm = monkeys[first]
        if second not in monkeys:
            monkeys[second] = OperationMonkey(second)
        sm = monkeys[second]
        if name not in monkeys:
            monkeys[name] = OperationMonkey(name)
        monkey = monkeys[name]
        monkey.set_info(fm, sm, operator)
    return monkeys


def find_humn_path(root: MathMonkey) -> bool | list[MathMonkey]:
    if isinstance(root, NumberMonkey):
        if root.name != "humn":
            return False
        else:
            return [root]
    elif isinstance(root, OperationMonkey):
        for m in root.first, root.second:
            humn_path = find_humn_path(m)
            if humn_path:
                return humn_path + [root]
        return False
    else:
        raise TypeError("unexpected monkey type")


def dive_in(root: OperationMonkey, humn_path: list, exp_val: int) -> int:
    if root.name == "humn":
        return exp_val
    match root.operator:
        case "+":
            if root.first in humn_path:
                return dive_in(root.first, humn_path, exp_val - root.second.return_val())
            else:
                return dive_in(root.second, humn_path, exp_val - root.first.return_val())
        case "-":
            if root.first in humn_path:
                return dive_in(root.first, humn_path, exp_val + root.second.return_val())
            else:
                return dive_in(root.second, humn_path, root.first.return_val() - exp_val)
        case "*":
            if root.first in humn_path:
                return dive_in(root.first, humn_path, exp_val // root.second.return_val())
            else:
                return dive_in(root.second, humn_path, exp_val // root.first.return_val())
        case "/":
            if root.first in humn_path:
                return dive_in(root.first, humn_path, exp_val * root.second.return_val())
            else:
                return dive_in(root.second, humn_path, root.first.return_val() // exp_val)


def part_a(data):
    nums, ops = parse(data)
    monkeys = init_monkeys(nums, ops)
    return monkeys["root"].return_val()


def part_b(data):
    nums, ops = parse(data)
    monkeys = init_monkeys(nums, ops)
    humn_path = find_humn_path(monkeys["root"])
    first, second = monkeys["root"].first, monkeys["root"].second
    if first not in humn_path:
        exp = first.return_val()
        start = second
    else:
        exp = second.return_val()
        start = first
    return dive_in(start, humn_path, exp)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=21)
    test = (
        """root: pppw + sjmn\n"""
        """dbpl: 5\n"""
        """cczh: sllz + lgvd\n"""
        """zczc: 2\n"""
        """ptdq: humn - dvpt\n"""
        """dvpt: 3\n"""
        """lfqf: 4\n"""
        """humn: 5\n"""
        """ljgn: 2\n"""
        """sjmn: drzm * dbpl\n"""
        """sllz: 4\n"""
        """pppw: cczh / lfqf\n"""
        """lgvd: ljgn * ptdq\n"""
        """drzm: hmdt - zczc\n"""
        """hmdt: 32\n"""
    )

    print("Part A")
    assert part_a(test) == 152
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 301
    print(part_b(puzzle.input_data))
