import collections
import functools
import itertools
import math
from collections import namedtuple
from typing import Tuple


class P3d():
    def __init__(self, x, y, z):
        self.c = [x, y, z]

    def __add__(self, other):
        return P3d(self.c[0] + other.c[0], self.c[1] + other.c[1], self.c[2] + other.c[2])

    def __sub__(self, other):
        return P3d(self.c[0] - other.c[0], self.c[1] - other.c[1], self.c[2] - other.c[2])

    def __repr__(self):
        return f"({','.join(self.c)})"


class Moon():
    def __init__(self, location: P3d):
        self.location = location
        self.velocity = P3d(0, 0, 0)

    def __repr__(self):
        return f"loc:{self.location} speed:{self.velocity}"

    def kin_energy(self):
        return sum([abs(x) for x in self.location.c]) * sum([abs(v) for v in self.velocity.c])


def gravity(mt: Tuple[Moon, ...]):
    m1, m2 = list(mt)
    for dim in range(3):
        if m1.location.c[dim] < m2.location.c[dim]:
            m1.velocity.c[dim] += 1
            m2.velocity.c[dim] -= 1
        elif m1.location.c[dim] > m2.location.c[dim]:
            m1.velocity.c[dim] -= 1
            m2.velocity.c[dim] += 1


def part_1(aoc_input, items):
    moons = []
    for line in aoc_input:
        parts = line[1:-1].split(', ')
        values = [int(p.split('=')[1]) for p in parts]
        moons.append(Moon(P3d(*values)))
    res = []
    tot_energy = sum([m.kin_energy() for m in moons])
    res.append(tot_energy)
    for _ in range(items):
        for pair in itertools.combinations(moons, 2):
            gravity(pair)
        for m in moons:
            m.location += m.velocity
        tot_energy = sum([m.kin_energy() for m in moons])
        res.append(tot_energy)
    return res


def test_1():
    aoc_input = [
        '<x=-1, y=0, z=2>',
        '<x=2, y=-10, z=-7>',
        '<x=4, y=-8, z=8>',
        '<x=3, y=5, z=-1>',
    ]
    res = part_1(aoc_input, 20)
    assert res[10] == 179


def merge(*iters):
    for it in iters:
        yield from it


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def part_2(aoc_input):
    moons = []
    for line in aoc_input:
        parts = line[1:-1].split(', ')
        values = [int(p.split('=')[1]) for p in parts]
        moons.append(Moon(P3d(*values)))
    state = [set() for _ in range(3)]
    for index, s in enumerate(state):
        s.add(tuple(list(merge(*[[m.location.c[index]] + [m.velocity.c[index]] for m in moons]))))
    steps = 1
    dim_step = []
    found = [False, False, False]
    while not all(f for f in found):
        for pair in itertools.combinations(moons, 2):
            gravity(pair)
        for m in moons:
            m.location += m.velocity
        for index, s in enumerate(state):
            mt = tuple(list(merge(*[[m.location.c[index]] + [m.velocity.c[index]] for m in moons])))
            if mt in state[index] and not found[index]:
                dim_step.append(steps)
                found[index] = True
            else:
                state[index].add(mt)
        steps += 1
    return functools.reduce(lcm, dim_step)


# <class 'list'>: [56344, 193052, 231614]

def test_2():
    aoc_input = [
        '<x=-1, y=0, z=2>',
        '<x=2, y=-10, z=-7>',
        '<x=4, y=-8, z=8>',
        '<x=3, y=5, z=-1>',
    ]
    res = part_2(aoc_input)
    assert res == 2772


def test_part2():
    aoc_input = [line.strip() for line in open('aoc2019_12_input.txt', 'r').readlines()]
    res = part_2(aoc_input)
    assert res == 314917503970904


def test_part1():
    aoc_input = [line.strip() for line in open('aoc2019_12_input.txt', 'r').readlines()]
    res = part_1(aoc_input, 1000000)
    assert res[1000] == 8960
