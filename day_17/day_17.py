#!/usr/bin/env python3
"""AOC 2022 day 17"""


from __future__ import annotations

import copy
from typing import List

import numpy as np
import pandas as pd
from aocd.models import Puzzle


def parse(data):
    return [d for d in data.strip()]


class Game:
    def __init__(self, data, rep_mem: int = 64, width: int = 7):
        self.width: int = width
        self.rock_count: int = 0
        self.horizontal_moves = 0
        self.highest: int = 0
        self.occupied: list = [[x, 0] for x in range(7)]
        self.movements: list = parse(data)
        self.rock_types: list = [HorizontalFour, Plus, Edge, VerticalFour, Square]
        self.memory: list = []
        self.rep_mem: int = rep_mem

    def new_rock(self, memorize: bool = False) -> None:
        nr = self.rock_types[self.rock_count % len(self.rock_types)](lowest=self.highest+4)
        while True:
            nr_copy = copy.deepcopy(nr)
            nr_copy.move_sideways(self.movements[jet_stream := self.horizontal_moves % len(self.movements)])
            if any(o in self.occupied for o in nr_copy.occupied):
                nr_copy = copy.deepcopy(nr)
                self.horizontal_moves += 1
            else:
                nr.move_sideways(self.movements[self.horizontal_moves % len(self.movements)])
                self.horizontal_moves += 1
            nr_copy.move_down()
            if any(o in self.occupied for o in nr_copy.occupied):
                break
            nr.move_down()
        self.highest = max(self.highest, max(o[1] for o in nr.occupied))
        self.occupied.extend(nr.occupied)
        self.rock_count += 1
        self.horizontal_moves %= len(self.movements)
        if memorize:
            self.memory.append(
                (
                    str(min(c[0] for c in nr.occupied)) + type(nr).__name__ + str(jet_stream),
                    self.rock_count,
                    self.highest
                )
            )

    def repetition_shortcut(self):
        if self.rock_count < 2*self.rep_mem:
            return None, None
        for i in range(self.rock_count-self.rep_mem+1):
            if [m[0] for m in self.memory[-self.rep_mem:]] == [m[0] for m in self.memory[i:i+self.rep_mem]]:
                rock_delta = self.memory[-self.rep_mem][1] - self.memory[i][1]
                height_delta = self.memory[-self.rep_mem][2] - self.memory[i][2]
                return rock_delta, height_delta

    def print_state(self, terminal_print: bool = False):
        arr = np.full((self.highest+1, 7), ".")
        for p in self.occupied:
            arr[self.highest-p[1], p[0]] = "#"
        df = pd.DataFrame(arr)
        np.savetxt(r'./tower.txt', df.values, fmt='%s')
        if terminal_print:
            print(df)


class Rock:
    def __init__(self) -> None:
        self.occupied: List[List[int, int]] = []

    def move_down(self) -> None:
        for o in self.occupied:
            o[1] -= 1

    def move_sideways(self, direction: str) -> None:
        match direction:
            case "<":
                if min(o[0] for o in self.occupied) == 0:
                    return
                move = -1
            case ">":
                if max(o[0] for o in self.occupied) == 6:
                    return
                move = 1
            case _:
                raise Exception("direction not defined")
        for o in self.occupied:
            o[0] += move


class VerticalFour(Rock):
    def __init__(self, lowest: int, left: int = 2) -> None:
        super().__init__()
        self.occupied = [[left, lowest], [left, lowest+1], [left, lowest+2], [left, lowest+3]]


class HorizontalFour(Rock):
    def __init__(self, lowest: int, left: int = 2) -> None:
        super().__init__()
        self.occupied = [[left, lowest], [left+1, lowest], [left+2, lowest], [left+3, lowest]]


class Square(Rock):
    def __init__(self, lowest: int, left: int = 2) -> None:
        super().__init__()
        self.occupied = [[left, lowest], [left+1, lowest], [left, lowest+1], [left+1, lowest+1]]


class Plus(Rock):
    def __init__(self, lowest: int, left: int = 2) -> None:
        super().__init__()
        self.occupied = [[left+1, lowest], [left+1, lowest+1], [left+1, lowest+2], [left, lowest+1], [left+2, lowest+1]]


class Edge(Rock):
    def __init__(self, lowest: int, left: int = 2) -> None:
        super().__init__()
        self.occupied = [[left, lowest], [left+1, lowest], [left+2, lowest], [left+2, lowest+1], [left+2, lowest+2]]


def part_a(data):
    game = Game(data)
    for _ in range(2022):
        game.new_rock()
    game.print_state()
    return game.highest


def part_b(data):
    game = Game(data)
    reps = 1000000000000
    height_shortcut = 0
    while game.rock_count <= reps:
        game.new_rock(memorize=True)
        rock_delta, height_delta = game.repetition_shortcut()
        if rock_delta:
            cycles = (reps - game.rock_count) // rock_delta
            rock_shortcut = cycles * rock_delta
            height_shortcut = cycles * height_delta
            for _ in range(reps - game.rock_count - rock_shortcut):
                game.new_rock()
            break
    return game.highest + height_shortcut


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=17)
    test = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>\n"""

    print("Part A")
    assert part_a(test) == 3068
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 1514285714288
    print(part_b(puzzle.input_data))
