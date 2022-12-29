#!/usr/bin/env python3
"""
AOC 2022 day 25
"""


from aocd.models import Puzzle


def parse(data: str) -> list:
    return [[i for i in l] for l in data.strip().split("\n")]


def solve(data: str) -> str:
    snafu_to_vals = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2,
    }
    vals_to_snafus = {v: k for k, v in snafu_to_vals.items()}
    snafus = parse(data)
    max_len = max(len(s) for s in snafus)
    readable = [[snafu_to_vals[e] for e in s] for s in snafus]
    snafu_sum = [0] * max_len
    for r in readable:
        for c, v in enumerate(r):
            snafu_sum[c + max_len - len(r)] += v
    res, over, over_mod = [], 0, 0
    for i in range(max_len-1, -1, -1):
        val = snafu_sum[i] + over
        over = (val + 2) // 5
        over_mod = (val + 2) % 5 - 2
        res.insert(0, over_mod)
    return "".join([vals_to_snafus[e] for e in res])


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=25)
    test = (
        """1=-0-2\n"""
        """12111\n"""
        """2=0=\n"""
        """21\n"""
        """2=01\n"""
        """111\n"""
        """20012\n"""
        """112\n"""
        """1=-1=\n"""
        """1-12\n"""
        """12\n"""
        """1=\n"""
        """122\n"""
    )

    print("Part A")
    assert solve(test) == "2=-1=0"
    print(solve(puzzle.input_data))
