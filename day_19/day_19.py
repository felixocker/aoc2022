#!/usr/bin/env python3
"""AOC 2022 day 19"""


import copy
import multiprocessing

from aocd.models import Puzzle


def parse(data) -> list:
    blueprints = []
    blueprint_data = [desc for desc in data.strip().split("\n")]
    for bd in blueprint_data:
        header, instructions = bd.split(": ")
        bpid = int(header.split("Blueprint ")[1])
        instructions = [instr for instr in instructions.split(".") if instr]
        robot_costs = {}
        for instr in instructions:
            eq = instr.split(" robot costs ")
            robot = eq[0].split()[1]
            costs = eq[1].split(" and ")
            robot_costs[robot] = {v: int(k) for k, v in [ingredients.split() for ingredients in costs]}
        blueprints.append((bpid, robot_costs))
    return blueprints


class RobotArmy:
    def __init__(self, blueprint: dict) -> None:
        self.raid, self.blueprint = blueprint
        self.robots = {
            "ore": 1,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        }
        self.resources = {
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        }
        self.max_required = {}
        for r in "ore", "clay", "obsidian":
            required = []
            for bp in self.blueprint:
                if r in self.blueprint[bp]:
                    required.append(self.blueprint[bp][r])
            self.max_required[r] = max(required)
        self.max_geodes = 0

    @staticmethod
    def mine(robots: dict, resources: dict) -> dict:
        for material in robots:
            resources[material] += robots[material]
        return resources

    def spend(self, resources: dict, robot: str) -> dict:
        if not robot:
            return resources
        for material in self.blueprint[robot]:
            if resources[material] < self.blueprint[robot][material]:
                raise ValueError
        for material in self.blueprint[robot]:
            resources[material] -= self.blueprint[robot][material]
        return resources

    @staticmethod
    def build(robots: dict, robot: str) -> dict:
        if not robot:
            return robots
        robots[robot] += 1
        return robots

    def optimize(self, reps: int, robots: dict, resources: dict, cache: set) -> set:
        cache_elem = str(reps) + str(robots) + str(resources)
        if cache_elem in cache:
            return cache
        cache.add(cache_elem)
        # break if max geodes not achievable anymore
        if resources["geode"] + robots["geode"] * reps + (reps + 1) * reps // 2 <= self.max_geodes:
            return cache
        for nxt in (None, "geode", "obsidian", "clay", "ore"):
            robots_cp, resources_cp = copy.copy(robots), copy.copy(resources)
            # obsidian requires ore and clay
            if nxt == "obsidian" and robots_cp["clay"] == 0:
                continue
            # geode requires ore and obsidian
            if nxt == "geode" and robots_cp["obsidian"] == 0:
                continue
            # break if max required can be provided
            if nxt in ("ore", "clay", "obsidian"):
                if robots_cp[nxt] >= self.max_required[nxt]:
                    continue
            try:
                resources_cp = self.spend(resources_cp, nxt)
            except ValueError:
                continue
            resources_cp = self.mine(robots_cp, resources_cp)
            robots_cp = self.build(robots_cp, nxt)
            self.max_geodes = max(self.max_geodes, resources_cp["geode"])
            if reps > 0:
                cache = self.optimize(reps-1, robots_cp, resources_cp, cache)
        return cache

    def quality_level(self, reps: int) -> int:
        self.optimize(reps, copy.copy(self.robots), copy.copy(self.resources), set())
        return self.raid * self.max_geodes

    def maximize_geodes(self, reps: int) -> int:
        self.optimize(reps, self.robots, self.resources, set())
        return self.max_geodes


def quality_level(task: tuple) -> int:
    robot_army, reps = task
    return robot_army.quality_level(reps)


def maximize_geodes(task: tuple) -> int:
    robot_army, reps = task
    return robot_army.maximize_geodes(reps)


def part_a(data, reps: int = 24) -> int:
    blueprints = parse(data)
    robot_armies = list(map(RobotArmy, blueprints))
    with multiprocessing.Pool() as pool:
        res = 0
        for result in pool.map(quality_level, zip(robot_armies, [reps]*len(robot_armies))):
            res += result
    return res


def part_b(data, reps: int = 32) -> int:
    blueprints = parse(data)[:3]
    robot_armies = list(map(RobotArmy, blueprints))
    with multiprocessing.Pool() as pool:
        res = 1
        for result in pool.map(maximize_geodes, zip(robot_armies, [reps]*len(robot_armies))):
            res *= result
    return res


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=19)
    test = (
        """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. """
        """Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.\n"""
        """Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. """
        """Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.\n"""
    )

    print("Part A")
    print(part_a(test))
    print(part_a(puzzle.input_data))

    print("Part B")
    print(part_b(test))
    print(part_b(puzzle.input_data))
