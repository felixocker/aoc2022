#!/usr/bin/env python3
"""
AOC 2022 day 22
NOTE: the solution for part b is input specific and may need to be adapted
it requires adding diagonals indicating how the cube's net is folded, cp the spreadsheet for examples
"""


import re

from aocd.models import Puzzle


def parse(data) -> tuple[list, list]:
    maze, instructions = data.split("\n\n")
    rows = maze.split("\n")
    max_x = max(len(r) for r in rows)
    maze = [[f for f in '{message: <{width}}'.format(message=r, width=max_x)] for r in rows]
    ins = re.split('(L|R)', instructions.strip())
    instructions = [int(i) if i.isnumeric() else i for i in ins]
    return maze, instructions


class Mover:
    def __init__(self, maze: list) -> None:
        self.maze = maze
        self.maze_dimensions = [len(maze), len(maze[0])]
        self.position = self._set_init()
        self.orientation = 0

    def _set_init(self) -> list[int, int]:
        for ci, i in enumerate(self.maze):
            for cj, _ in enumerate(i):
                if self.maze[ci][cj] == ".":
                    return [ci, cj]

    def turn(self, direction: str) -> None:
        assert direction in ("L", "R")
        match direction:
            case "R":
                self.orientation = (self.orientation + 1) % 4
            case "L":
                self.orientation = (self.orientation - 1) % 4

    def move(self, steps: int, trace: bool = False) -> None:
        """move forward with current orientation, possibly across edges
        :param steps: number of steps to be moved in current orientation
        :param trace: track moves by storing orientation into maze fields
        """
        dirs = {
            0: (0, 1),
            1: (1, 0),
            2: (0, -1),
            3: (-1, 0),
        }
        x, y = self.position
        o = self.orientation
        while steps > 0:
            steps -= 1
            if trace:
                self.maze[x][y] = str(o)
            x = (x + dirs[o][0]) % self.maze_dimensions[0]
            y = (y + dirs[o][1]) % self.maze_dimensions[1]
            if self.maze[x][y] == "#":
                break
            elif self.maze[x][y] == " ":
                steps += 1
            elif self.maze[x][y] == ".":
                self.position = [x, y]
                self.orientation = o
            elif self.maze[x][y] == "u":
                steps += 1
                if o in (0, 2):
                    o = (o + 1) % 4
                elif o in (1, 3):
                    o = (o - 1) % 4
            elif self.maze[x][y] == "d":
                steps += 1
                if o in (0, 2):
                    o = (o - 1) % 4
                elif o in (1, 3):
                    o = (o + 1) % 4


def part_a(data):
    maze, instructions = parse(data)
    mover = Mover(maze)
    for i in instructions:
        if isinstance(i, int):
            mover.move(i)
        elif isinstance(i, str):
            mover.turn(i)
    row, column = mover.position
    facing = mover.orientation
    return 1000 * (row + 1) + 4 * (column + 1) + facing


def preprocess_b(maze: list, edge_len: int, starts_down: tuple, starts_up: tuple, top_padding: int, bottom_padding: int,
                 full_width: int, height: int, left_padding: int, right_padding: int) -> list:
    """add turning points to test case
    # NOTE: hard-coded for my specific input
    :param maze: list representation of the maze created by the parse function
    :param edge_len: length of the cube's edges
    :param starts_down: coordinates for the top left corners of the areas (with width = edge_len) containing the
        diagonals pointing to the bottom right
    :param starts_up: coordinates for the top left corners of the areas (with width = edge_len) containing the
        diagonals pointing to the top right
    """

    def _turning_diagonal_down(maze: list, top_left_corner: tuple, ln: int) -> None:
        sx, sy = top_left_corner
        for i in range(ln):
            maze[sx + i][sy + i] = "d"

    def _turning_diagonal_up(maze: list, top_left_corner: tuple, ln: int) -> None:
        sx, sy = top_left_corner
        for i in range(ln):
            maze[sx + ln - 1 - i][sy + i] = "u"

    # add padding to sides
    for r in range(height*edge_len):
        for _ in range(left_padding*edge_len):
            maze[r].insert(0, " ")
        for _ in range(right_padding*edge_len):
            maze[r].append(" ")
    # add padding to top
    for _ in range(top_padding*edge_len):
        maze.insert(0, [" "] * full_width*edge_len)
    # add padding to bottom
    for _ in range(bottom_padding*edge_len):
        maze.append([" "] * full_width*edge_len)
    # add diagonals w turning indicators
    for sd in starts_down:
        _turning_diagonal_down(maze, sd, edge_len)
    for su in starts_up:
        _turning_diagonal_up(maze, su, edge_len)
    return maze


def part_b(data, testcase: bool, trace: bool = False):
    """run part b for the testcase and my individual input
    NOTE: this requires bespoke preprocessing - add padding with turning points, cp spreadsheet
    :param data: input data consisting of the maze and the moving instructions
    :param testcase: indicator for custom preprocessing
    :param trace: trace orientation along path and print to file - this may interfere with the results though
    """
    maze, instructions = parse(data)
    if testcase:
        cube_len = 4
        starts_down = ((0, 4), (4, 8), (8, 0), (12, 20), (16, 12), (20, 16))
        starts_up = ((0, 12), (20, 0), (16, 4), (12, 8), (8, 16), (4, 20))
        top_padding, left_padding = 1, 1
        maze = preprocess_b(maze, cube_len, starts_down, starts_up, top_padding=top_padding, bottom_padding=2,
                            full_width=6, height=3, left_padding=left_padding, right_padding=1)
    else:
        cube_len = 50
        starts_down = ((0, 0), (50, 50), (100, 100), (150, 150), (250, 200), (300, 150), (150, 250), (200, 300))
        starts_up = ((50, 200), (0, 250), (100, 300), (300, 0), (250, 50), (200, 100))
        top_padding, left_padding = 2, 3
        maze = preprocess_b(maze, cube_len, starts_down, starts_up, top_padding=top_padding, bottom_padding=1,
                            full_width=7, height=4, left_padding=left_padding, right_padding=1)
    mover = Mover(maze)
    for i in instructions:
        if isinstance(i, int):
            mover.move(i, trace)
        elif isinstance(i, str):
            mover.turn(i)
    row, column = mover.position
    facing = mover.orientation
    # consider padding for coordinates
    row = row - top_padding * cube_len
    column = column - left_padding * cube_len
    if trace:
        with open("out.txt", "w") as f:
            f.write("\n".join("".join(i) for i in maze))
    return 1000 * (row + 1) + 4 * (column + 1) + facing


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=22)
    test = (
        """        ...#\n"""
        """        .#..\n"""
        """        #...\n"""
        """        ....\n"""
        """...#.......#\n"""
        """........#...\n"""
        """..#....#....\n"""
        """..........#.\n"""
        """        ...#....\n"""
        """        .....#..\n"""
        """        .#......\n"""
        """        ......#.\n"""
        """\n"""
        """10R5L5R10L4R5L5\n"""
    )

    print("Part A")
    assert part_a(test) == 6032
    print(part_a(puzzle.input_data))

    print("Part B")
    assert part_b(test, testcase=True) == 5031
    print(part_b(puzzle.input_data, testcase=False))
