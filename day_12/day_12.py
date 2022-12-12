#!/usr/bin/env python3
"""AOC 2022 day 12"""


import heapq
import itertools
import string

import numpy as np
from aocd.models import Puzzle


def parse(data) -> np.array:
    raw_map = [[p for p in l] for l in data.split("\n") if l]
    np_map = np.array(raw_map, dtype=np.dtype('U100'))
    return np.pad(np_map, 1, 'constant', constant_values="0")


def find(my_map: np.array) -> tuple:
    start = np.where(my_map == "S")
    end = np.where(my_map == "E")
    return (start[0][0], start[1][0]), (end[0][0], end[1][0])


def preprocess_map(my_map: np.array) -> np.array:
    char_to_val = {char: c+1 for c, char in enumerate(string.ascii_lowercase)}
    char_to_val["S"] = 1
    char_to_val["E"] = 26
    for cx, vx in enumerate(my_map):
        for cy, vy in enumerate(vx):
            if vy == "0":
                continue
            if vy in char_to_val:
                my_map[cx][cy] = char_to_val[vy]
    return my_map.astype(int)


def move(pos: tuple, my_map: np.array):
    x, y = pos
    for m in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        new = x+m[0], y+m[1]
        nxt_val = my_map[new[0]][new[1]]
        if not nxt_val == 0 and nxt_val - my_map[x][y] <= 1:
            yield new


def dijkstra(padded_map: np.array, start: tuple, end: tuple) -> int:
    nodes = [(i, j) for i in range(1, padded_map.shape[0]-1) for j in range(1, padded_map.shape[1]-1)]
    distances = {n: float("inf") for n in nodes}
    priors = {n: None for n in nodes}
    distances[start] = 0
    node_heap = []
    entry_finder = {}
    counter = itertools.count()
    for n in nodes:
        add_node_to_heap(node_heap, n, counter, entry_finder, priority=distances[n])
    while end in entry_finder:
        closest = pop_node_from_heap(node_heap, entry_finder)
        for nxt in move(closest, padded_map):
            if nxt in entry_finder:
                update_distance(closest, nxt, distances, priors, node_heap, counter, entry_finder)
    return distances[end]


def add_node_to_heap(my_heap: list, node: tuple, counter: itertools.count, entry_finder: dict, priority=0) -> None:
    if node in entry_finder:
        remove_node_from_heap(node, entry_finder)
    count = next(counter)
    entry = [priority, count, node]
    entry_finder[node] = entry
    heapq.heappush(my_heap, entry)


def remove_node_from_heap(node: tuple, entry_finder: dict) -> None:
    entry = entry_finder.pop(node)
    entry[-1] = (None, None)


def pop_node_from_heap(my_heap: list, entry_finder: dict) -> tuple:
    while my_heap:
        priority, count, node = heapq.heappop(my_heap)
        if node != (None, None):
            del entry_finder[node]
            return node
    raise KeyError("Cannot pop from empty priority queue")


def update_distance(closest, nxt, distances, priors, node_heap, counter, entry_finder) -> None:
    alternative = distances[closest] + 1
    if alternative < distances[nxt]:
        distances[nxt] = alternative
        priors[nxt] = closest
        remove_node_from_heap(nxt, entry_finder)
        add_node_to_heap(node_heap, nxt, counter, entry_finder, alternative)


def part_a(data) -> int:
    padded_map = parse(data)
    start, end = find(padded_map)
    processed_map = preprocess_map(padded_map)
    return dijkstra(processed_map, start, end)


def part_b(data) -> int:
    padded_map = parse(data)
    _, end = find(padded_map)
    processed_map = preprocess_map(padded_map)
    starts = list(zip(*np.where(processed_map == 1)))
    path_lengths = [dijkstra(processed_map, start, end) for start in starts]
    return min(path_lengths)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=12)
    test = """Sabqponm\nabcryxxl\naccszExk\nacctuvwj\nabdefghi\n"""

    print("Part A")
    assert part_a(test) == 31
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 29
    print(part_b(puzzle.input_data))
