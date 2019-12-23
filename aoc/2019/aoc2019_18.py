import copy
import math
from collections import defaultdict
from aoc import P

maze = """
######
#b@.B#
######
"""[1:-1]

def tree_from_map(the_map):
    tree = defaultdict(set)
    for k in [k for k in the_map.keys() if the_map[k] != '#']:
        for reachable in [p for p in k.nesw() if the_map[p] != '#']:
            tree[k].add(reachable)
            tree[reachable].add(k)
    return tree

def tunnel_map(lines):
    the_map = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            the_map[P(x, y)] = char
    return the_map

def read_tunnels_fromfile(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return tunnel_map(lines)

def test_tree():
    tree = tree_from_map(tunnel_map(maze.split('\n')))
    assert tree == {P(x=1, y=1): {P(x=2, y=1)},
                    P(x=2, y=1): {P(x=3, y=1), P(x=1, y=1)},
                    P(x=3, y=1): {P(x=4, y=1), P(x=2, y=1)},
                    P(x=4, y=1): {P(x=3, y=1)}}

def test_tunnel_map():
    tm = tunnel_map(maze.split('\n'))
    assert tm == {P(x=0, y=0): '#', P(x=0, y=1): '#', P(x=0, y=2): '#',
                  P(x=1, y=0): '#', P(x=1, y=1): 'b', P(x=1, y=2): '#',
                  P(x=2, y=0): '#', P(x=2, y=1): '@', P(x=2, y=2): '#',
                  P(x=3, y=0): '#', P(x=3, y=1): '.', P(x=3, y=2): '#',
                  P(x=4, y=0): '#', P(x=4, y=1): 'B', P(x=4, y=2): '#',
                  P(x=5, y=0): '#', P(x=5, y=1): '#', P(x=5, y=2): '#'}

def reachable_keys(tree, tunmap):
    reachable_keys = []
    cur_loc = [k for k in tree.keys() if tunmap[k] == '@'][0]
    tocheck = {cur_loc}
    seen = set()
    while tocheck:
        k = tocheck.pop()
        seen.add(k)
        for canreach in [p for p in tree[k] if p not in seen]:
            if tunmap[canreach].islower():
                reachable_keys.append(canreach)
            elif tunmap[canreach] == '.':
                tocheck.add(canreach)
    return reachable_keys

def shortest_path(tree, tunmap, A, B):
    tocheck = {(A, 0)}
    seen = set()
    mindist = math.inf
    while tocheck:
        k, dist = tocheck.pop()
        seen.add(k)
        for canreach in [p for p in tree[k] if p not in seen and (tunmap[p].islower() or tunmap[p] == '.')]:
            if canreach == B:
                mindist = min(mindist, dist + 1)
            else:
                tocheck.add((canreach, dist + 1))
    return mindist

def steps_to_remove_keys(tree, tunmap):
    cur_loc = [k for k in tree.keys() if tunmap[k] == '@'][0]
    minsteps = math.inf
    for key in reachable_keys(tree, tunmap):
        dup_tunmap = copy.deepcopy(tunmap)
        steps_needed = shortest_path(tree, tunmap, cur_loc, key)
        doorlist = [k for k in tunmap.keys() if tunmap[k] == tunmap[key].upper()]
        if doorlist:
            dup_tunmap[doorlist[0]] = '.'
        dup_tunmap[cur_loc] = '.'
        dup_tunmap[key] = '@'
        # if reachable_keys(tree, dup_tunmap):
        if any(c.islower() for c in dup_tunmap.values()):
            steps_needed += steps_to_remove_keys(tree, dup_tunmap)
        minsteps = min(minsteps, steps_needed)
    return minsteps

def test_aoc1():
    maze = """
#########
#b.A.@.a#
#########
"""[1:-1]
    tunmap = tunnel_map(maze.split('\n'))
    tree = tree_from_map(tunmap)
    min_steps = steps_to_remove_keys(tree, tunmap)
    assert min_steps == 8

def test_aoc2():
    maze = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""[1:-1]
    tunmap = tunnel_map(maze.split('\n'))
    tree = tree_from_map(tunmap)
    min_steps = steps_to_remove_keys(tree, tunmap)
    assert min_steps == 86

def test_part1():
    tunmap = read_tunnels_fromfile('aoc2019_18_input.txt')
    tree = tree_from_map(tunmap)
    min_steps = steps_to_remove_keys(tree, tunmap)
    assert min_steps == 86

