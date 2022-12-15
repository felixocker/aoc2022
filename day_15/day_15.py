#!/usr/bin/env python3
"""AOC 2022 day 15"""


from aocd.models import Puzzle


def parse(data) -> list:
    raw = [[e.split(", ") for e in l.split(": ")] for l in data.strip().split("\n")]
    coords = [[(int(e[0].split("x=")[1]), int(e[1].split("y=")[1])) for e in r] for r in raw]
    return coords


class Area:

    def __init__(self, sensor: tuple, beacon: tuple, row_of_interest: int) -> None:
        self.sensor = sensor
        self.beacon = beacon
        self.dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        self.row_of_interest = row_of_interest

    def rule_out(self) -> set:
        """find positions a beacon cannot be in"""
        covered = set()
        sx, sy = self.sensor
        for y in range(sy - self.dist, sy + self.dist + 1):
            if y == self.row_of_interest:
                for x in range(sx - self.dist, sx + self.dist + 1):
                    if abs(x-sx) + abs(y-sy) <= self.dist:
                        covered.add((x, y))
        return covered

    def rule_out_range(self) -> list | None:
        """check overlap of area scanned by sensor and row of interest"""
        vdist = (self.dist - abs(self.row_of_interest - self.sensor[1]))
        if abs(self.sensor[1]-self.row_of_interest) > self.dist:
            return None
        return [self.sensor[0]-vdist, self.sensor[0]+vdist]


def combine_ranges(ranges: list) -> list | int:
    """return either the combined ranges or the index of the missing part"""
    ranges.sort()
    merge = ranges[0]
    for r in ranges[1:]:
        if r[0] <= merge[1]:
            if merge[1] <= r[1]:
                merge[1] = r[1]
        else:
            return r[0]-1
    return merge


def part_a(data, row_of_interest: int) -> int:
    coords = parse(data)
    ruled_out_positions, ignore = set(), set()
    for sensor, beacon in coords:
        area = Area(sensor, beacon, row_of_interest)
        ruled_out_positions.update(area.rule_out())
        for p in area.sensor, area.beacon:
            if p[1] == row_of_interest:
                ignore.add(p)
    return len(ruled_out_positions - ignore)


def part_b(data, square: int):
    coords = parse(data)
    for roi in range(square+1):
        ruled_out_ranges = []
        for sensor, beacon in coords:
            area = Area(sensor, beacon, roi)
            if (rng := area.rule_out_range()) is not None:
                ruled_out_ranges.append(rng)
        row = combine_ranges(ruled_out_ranges)
        if isinstance(row, int):
            return row * 4000000 + roi
        elif row[0] > 0:
            return roi
        elif row[1] < square:
            return square * 4000000 + roi


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=15)
    test = (
        """Sensor at x=2, y=18: closest beacon is at x=-2, y=15\n"""
        """Sensor at x=9, y=16: closest beacon is at x=10, y=16\n"""
        """Sensor at x=13, y=2: closest beacon is at x=15, y=3\n"""
        """Sensor at x=12, y=14: closest beacon is at x=10, y=16\n"""
        """Sensor at x=10, y=20: closest beacon is at x=10, y=16\n"""
        """Sensor at x=14, y=17: closest beacon is at x=10, y=16\n"""
        """Sensor at x=8, y=7: closest beacon is at x=2, y=10\n"""
        """Sensor at x=2, y=0: closest beacon is at x=2, y=10\n"""
        """Sensor at x=0, y=11: closest beacon is at x=2, y=10\n"""
        """Sensor at x=20, y=14: closest beacon is at x=25, y=17\n"""
        """Sensor at x=17, y=20: closest beacon is at x=21, y=22\n"""
        """Sensor at x=16, y=7: closest beacon is at x=15, y=3\n"""
        """Sensor at x=14, y=3: closest beacon is at x=15, y=3\n"""
        """Sensor at x=20, y=1: closest beacon is at x=15, y=3\n"""
    )

    print("Part A")
    assert part_a(test, 10) == 26
    print(part_a(puzzle.input_data, 2000000))

    print("Part B")
    assert part_b(test, 20) == 56000011
    print(part_b(puzzle.input_data, 4000000))
