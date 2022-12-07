#!/usr/bin/env python3
"""AOC 2022 day 7"""


from __future__ import annotations

from aocd.models import Puzzle


class File:

    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


class Folder:

    def __init__(self, name: str, parent: Folder):
        self.name = name
        self.parent = parent
        self.files = {}
        self.folders = {}
        self.size = None

    def add_content(self, content) -> None:
        if isinstance(content, Folder):
            self.folders[content.name] = content
        elif isinstance(content, File):
            self.files[content.name] = content

    def update_size(self):
        files_size = sum([self.files[f].size for f in self.files])
        folders_size = sum([self.folders[f].update_size() for f in self.folders])
        self.size = files_size + folders_size
        return self.size


def parse(data) -> Folder:
    lines = [l for l in data.split("\n") if l[:4]]
    root = Folder(name="/", parent=None)
    current_folder = root
    for l in lines[1:]:
        if l == "$ cd ..":
            current_folder = current_folder.parent
        elif l == "$ cd /":
            current_folder = root
        elif l[:5] == "$ cd ":
            current_folder = current_folder.folders[l[5:]]
        elif l == "$ ls":
            continue
        elif l[:4] == "dir ":
            dname = l[4:]
            d = Folder(name=dname, parent=current_folder)
            current_folder.add_content(d)
        else:
            size, fname = l.split()
            f = File(name=fname, size=int(size))
            current_folder.add_content(f)
    return root


def part_a(data) -> int:
    root = parse(data)
    root.update_size()

    def _dive_in(folder: Folder) -> int:
        sum_of_sizes = 0
        if folder.size <= 100000:
            sum_of_sizes += folder.size
        for subfolder in folder.folders.values():
            sum_of_sizes += _dive_in(subfolder)
        return sum_of_sizes

    return _dive_in(root)


def part_b(data) -> int:
    root = parse(data)
    root.update_size()

    required_size = 30000000 - (70000000 - root.size)
    assert root.size >= required_size, "not enough disk space available"

    def _dive_in(folder: root, smallest: int) -> int:
        for subfolder in folder.folders.values():
            if subfolder.size >= required_size:
                smallest = min(smallest, _dive_in(subfolder, subfolder.size))
        return smallest

    return _dive_in(root, root.size)


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=7)
    with open("test.txt") as f:
        txt = f.read()

    assert part_a(txt) == 95437, "calculating sum of sizes failed"
    print("Part A")
    print(part_a(puzzle.input_data))

    assert part_b(txt) == 24933642, "finding size of directory to be deleted failed"
    print("Part B")
    print(part_b(puzzle.input_data))
