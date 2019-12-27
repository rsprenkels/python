import copy
import math
from collections import defaultdict, deque
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


def steps_all_keys(tree, tun_map):
    cur_loc = [k for k in tree.keys() if tun_map[k] == '@'][0]
    all_keys = {tun_map[k] for k in tree.keys() if tun_map[k].islower()}
    minsteps = math.inf
    seen = set()
    queue = deque()
    queue.append((cur_loc, 0, set()))
    while queue:
        node, dist, keyset = queue.popleft()
        seen.add((node, frozenset(keyset)))
        for reachable in tree[node]:
            if tun_map[reachable].islower():
                newkeyset = keyset | set(tun_map[reachable])
                if newkeyset == all_keys:
                    if dist + 1 < minsteps:
                        minsteps = dist + 1
                elif (reachable, frozenset(newkeyset)) not in seen:
                    queue.append((reachable, dist + 1, newkeyset))
            elif tun_map[reachable].isupper():
                if tun_map[reachable].lower() in keyset and (reachable, frozenset(keyset)) not in seen:
                    queue.append((reachable, dist + 1, keyset))
            elif (reachable, frozenset(keyset)) not in seen:
                queue.append((reachable, dist + 1, keyset))
    return minsteps



def test_aoc1():
    maze = """
#########
#b.A.@.a#
#########
"""[1:-1]
    tunmap = tunnel_map(maze.split('\n'))
    tree = tree_from_map(tunmap)
    min_steps = steps_all_keys(tree, tunmap)
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
    min_steps = steps_all_keys(tree, tunmap)
    assert min_steps == 86

def test_part1():
    tunmap = read_tunnels_fromfile('aoc2019_18_input.txt')
    tree = tree_from_map(tunmap)
    min_steps = steps_all_keys(tree, tunmap)
    assert min_steps == 4590

