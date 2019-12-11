import copy
import functools
import math
from collections import namedtuple
from typing import Set, Tuple, Optional, Any, List


class P(namedtuple('Point', ['x', 'y'])):
    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    def normal(self):
        if self.x == 0:
            return P(0, self.y // abs(self.y))
        elif self.y == 0:
            return P(self.x // abs(self.x), 0)
        else:
            return P(self.x // math.gcd(self.x, self.y), self.y // math.gcd(self.x, self.y))


def test_v1():
    assert P(12, 0).normal() == P(1, 0)
    assert P(-10, 0).normal() == P(-1, 0)
    assert P(0, 16).normal() == P(0, 1)
    assert P(0, -2316).normal() == P(0, -1)


def test_v2():
    assert P(3, 4) - P(2, 1) == P(1, 3)


def test_v3():
    assert (P(3, 4) - P(2, 1)).normal() == P(1, 3)
    assert P(4, 2).normal() == P(2, 1)


def readmap(filename: str) -> Tuple[Set[P], int, int]:
    with open(filename, 'r') as f:
        input = f.read().split('\n')
    astmap = set()
    map_h = len(input)
    map_w = len(input[0])
    for y, line in enumerate(input):
        for x, mapchar in enumerate(line):
            if mapchar == '#':
                astmap.add((P(x, y)))
    return (astmap, map_w, map_h)


def best_pos(astmap) -> Tuple[Optional[Any], int]:
    max_visible = 0
    best_point = None
    for ast in astmap:
        v = get_visible(astmap, ast)
        if len(v) > max_visible:
            best_point = ast
            max_visible = len(v)
    return best_point, max_visible


def get_visible(astmap, viewpoint):
    m = copy.deepcopy(astmap)
    m.remove(viewpoint)
    for other in astmap:
        if other == viewpoint:
            continue
        step = (other - viewpoint).normal()
        point = viewpoint + step
        while point != other:
            if point in astmap:
                m.remove(other)
                break
            point += step
    return m


def vapourize_order(astmap) -> List[P]:
    monitor_station = best_pos(astmap)[0]
    origin = monitor_station
    refvec = P(0, -1)
    sort_order = functools.partial(clockwiseangle_and_distance, origin=origin, refvec = refvec)
    vap_order = []
    while len(astmap) > 1:
        visible_set = get_visible(astmap, monitor_station)
        for ast in sorted(visible_set, key=sort_order):
            vap_order.append(ast)
        astmap = astmap - visible_set
    return vap_order

# https://stackoverflow.com/questions/41855695/sorting-list-of-two-dimensional-coordinates-by-clockwise-angle-using-python
def clockwiseangle_and_distance(point: P, origin, refvec) -> Tuple[float, float]:
    # Vector between point and the origin: v = p - o
    vector = point - origin
    # Length of vector: ||v||
    lenvector = math.hypot(vector.x, vector.y)
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = P(vector.x / lenvector, vector.y / lenvector)
    dotprod = normalized.x * refvec.x + normalized.y * refvec.y  # x1*x2 + y1*y2
    diffprod = refvec.y * normalized.x - refvec.x * normalized.y  # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle <= 0:
        return -angle, lenvector
    return 2 * math.pi - angle, lenvector


def test_sort_1():
    origin = P(0, 0)
    refvec = P(0, 1)
    sort_order = functools.partial(clockwiseangle_and_distance, origin=origin, refvec = refvec)
    assert sort_order(P(0, 10)) == (0.0, 10.0)

def test_sort2():
    pts = [P(-2, 1), P(1, -1), P(-3, -1), P(5, -6), P(1, 3), P(6, -5), P(2, 5)]
    origin = P(0, 0)
    refvec = P(0, 1)
    sort_order = functools.partial(clockwiseangle_and_distance, origin=origin, refvec = refvec)
    assert sorted(pts, key=sort_order) == \
           [P(1, 3), P(2, 5), P(6, -5), P(1, -1), P(5, -6), P(-3, -1), P(-2, 1)]


def test_1():
    m, w, h = readmap('aoc2019_10_test1.txt')
    assert best_pos(m) == ((5, 8), 33)


def test_part1():
    m, w, h = readmap('aoc2019_10_input.txt')
    assert best_pos(m) == ((19, 14), 274)


def test_part2_testdata():
    m, w, h = readmap('aoc2019_10_test2.txt')
    order = vapourize_order(m)
    assert order[199] == P(8, 2)


def test_part2():
    m, w, h = readmap('aoc2019_10_input.txt')
    order = vapourize_order(m)
    assert order[199] == P(3, 5)


if __name__ == '__main__':
    m, w, h = readmap('aoc2019_10_input.txt')
    print(f"aoc 2019 day 10 part 1 {best_pos(m)[1]}")
    p = vapourize_order(m)[199]
    print(f"aoc 2019 day 10 part 2 {p.x * 100 + p.y}")




