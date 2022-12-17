#!/usr/bin/env python3
"""AOC 2022 day 16"""


from typing import Tuple

from aocd.models import Puzzle


class Valve:

    def __init__(self, vid: int, name: str, rate: int) -> None:
        self.name = name
        self.vid = vid
        self.rate = rate
        self.connections = []


def parse(data) -> Tuple[list, list, Valve]:
    valve_data = [l.split("; ") for l in data.strip().split("\n")]
    valves, relevant_valves, start_valve = list(), list(), None
    for c, vd in enumerate(valve_data):
        valve = vd[0][6:8]
        flow_rate = int(vd[0].split("=")[1])
        valves.append(v := Valve(c, valve, flow_rate))
        if flow_rate > 0:
            relevant_valves.append(v)
        if valve == "AA":
            start_valve = v
    for c, vd in enumerate(valve_data):
        if "valves" in vd[1]:
            tunnels_to = vd[1].split("valves ")[1].split(", ")
        else:
            tunnels_to = [vd[1].split("valve ")[1]]
        valves[c].connections.extend(v for v in valves if v.name in tunnels_to)
    return valves, relevant_valves, start_valve


class DistanceFinder:

    def __init__(self, valves: list) -> None:
        self.valves = valves
        self.ln = len(valves)
        self.dists = [[float("inf")] * self.ln for _ in range(self.ln)]

    def build(self) -> None:
        """use floyd-warshall algorithm"""
        for v in self.valves:
            for e in v.connections:
                self.dists[v.vid][e.vid] = 1
        for i in range(self.ln):
            self.dists[i][i] = 0
        for k in range(self.ln):
            for i in range(self.ln):
                for j in range(self.ln):
                    if self.dists[i][j] > self.dists[i][k] + self.dists[k][j]:
                        self.dists[i][j] = self.dists[i][k] + self.dists[k][j]


class Solver:

    def __init__(self, relevant_valves: list, distances: list) -> None:
        self.relevant_valves = relevant_valves
        self.dists = distances
        self.solutions = []

    def release_pressure(self, current: Valve, score: int, time: int, visited: list, deadline: int, remember: bool) -> int:
        if remember:
            self.solutions.append([score, visited])
        vals = []
        for v in self.relevant_valves:
            new_time = time + self.dists[current.vid][v.vid] + 1
            new_score = score + v.rate * (deadline - new_time)
            if v is not current and new_time <= deadline and v.vid not in visited:
                vals.append(self.release_pressure(v, new_score, new_time, visited + [v.vid], deadline, remember))
        if not vals:
            return score
        return max(vals)


def part_a(data) -> int:
    valves, relevant_valves, start_valve = parse(data)
    df = DistanceFinder(valves)
    df.build()
    solver_a = Solver(relevant_valves, df.dists)
    return solver_a.release_pressure(start_valve, 0, 0, [], 30, False)


def part_b(data) -> int:
    valves, relevant_valves, start_valve = parse(data)
    df = DistanceFinder(valves)
    df.build()
    solver_b = Solver(relevant_valves, df.dists)
    single_sol = solver_b.release_pressure(start_valve, 0, 0, [], 26, True)
    best_sol = single_sol
    for s in solver_b.solutions:
        if best_sol - s[0] >= single_sol:
            continue
        elephant_score = solver_b.release_pressure(start_valve, s[0], 0, s[1], 26, False)
        best_sol = max(best_sol, elephant_score)
    return best_sol


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=16)
    test = (
        """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB\n"""
        """Valve BB has flow rate=13; tunnels lead to valves CC, AA\n"""
        """Valve CC has flow rate=2; tunnels lead to valves DD, BB\n"""
        """Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE\n"""
        """Valve EE has flow rate=3; tunnels lead to valves FF, DD\n"""
        """Valve FF has flow rate=0; tunnels lead to valves EE, GG\n"""
        """Valve GG has flow rate=0; tunnels lead to valves FF, HH\n"""
        """Valve HH has flow rate=22; tunnel leads to valve GG\n"""
        """Valve II has flow rate=0; tunnels lead to valves AA, JJ\n"""
        """Valve JJ has flow rate=21; tunnel leads to valve II\n"""
    )

    print("Part A")
    assert part_a(test) == 1651
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test) == 1707
    print(part_b(puzzle.input_data))
