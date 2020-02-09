import math
from collections import namedtuple, defaultdict

from aoc import *


def tmap(lines):
    grid = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[P(x, y)] = char
    nonwalls = [p for p in grid.keys() if grid[p] != '#']
    tree = defaultdict(list)
    for p in nonwalls:
        print(f"{p} is a nonwall {grid[p]}")


def read_tmap_fromfile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return tmap(lines)


def test_tm():
    lines = """
#########
#b.A.@.a#
#########
"""[1:-1]
    tm = tmap(lines.split('\n'))
    assert tm == None