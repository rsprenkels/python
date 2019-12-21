import math
from collections import namedtuple


class P(namedtuple('Point', ['x', 'y'])):

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    def right(self):
        return {P(0, 1): P(1, 0), P(1, 0): P(0, -1), P(0, -1): P(-1, 0), P(-1, 0): P(0, 1)}[self]

    def left(self):
        return {P(0, 1): P(-1, 0), P(1, 0): P(0, 1), P(0, -1): P(1, 0), P(-1, 0): P(0, -1)}[self]

    def normal(self):
        if self.x == 0:
            return P(0, self.y // abs(self.y))
        elif self.y == 0:
            return P(self.x // abs(self.x), 0)
        else:
            return P(self.x // math.gcd(self.x, self.y), self.y // math.gcd(self.x, self.y))


def tunnel_map(lines):
    the_map = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            the_map[P(x, y)] = char
    return the_map


def read_tunnels_fromfile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return tunnel_map(lines)


def test_tm():
    lines = """
#########
#b.A.@.a#
#########
"""[1:-1]
    tm = tunnel_map(lines.split('\n'))
    assert tm == None