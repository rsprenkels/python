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


def reachable_keys(tree, tun_map):
    r_keys = []
    cur_loc = [k for k in tree.keys() if tun_map[k] == '@'][0]
    to_check = {cur_loc}
    seen = set()
    while to_check:
        k = to_check.pop()
        seen.add(k)
        for can_reach in [p for p in tree[k] if p not in seen]:
            if tun_map[can_reach].islower():
                r_keys.append(can_reach)
            elif tun_map[can_reach] == '.':
                to_check.add(can_reach)
    return r_keys


def shortest_path(tree, tunmap, a, b):
    to_check = {(a, 0)}
    seen = set()
    min_dist = math.inf
    while to_check:
        k, dist = to_check.pop()
        seen.add(k)
        for can_reach in [p for p in tree[k] if p not in seen and (tunmap[p].islower() or tunmap[p] == '.')]:
            if can_reach == b:
                min_dist = min(min_dist, dist + 1)
            else:
                to_check.add((can_reach, dist + 1))
    return min_dist


def steps_to_remove_keys(tree, tun_map):
    cur_loc = [k for k in tree.keys() if tun_map[k] == '@'][0]
    min_steps = math.inf
    rk = reachable_keys(tree, tun_map)
    dup_tun_map = copy.deepcopy(tun_map)
    for k in rk:
        dup_tun_map[k] = '.'  # remove keys
    for dk in [dk for dk in tun_map.keys() if tun_map[dk] in [tun_map[k].upper() for k in rk]]:
        dup_tun_map[dk] = '.'  # remove doors
    rk_with_doors_open = reachable_keys(dup_tun_map)
    # find the most nearby key
    min_dist = math.inf
    last_key = None
    for k in rk_with_doors_open:
        for start_pos in rk:
            dist = shortest_path(tree, tun_map, start_pos, k)
            if dist < min_dist:
                min_dist = dist
                last_key = start_pos

    for key in rk:
        steps_needed = shortest_path(tree, tun_map, cur_loc, key)
        doorlist = [k for k in tun_map.keys() if tun_map[k] == tun_map[key].upper()]
        if doorlist:
            dup_tun_map[doorlist[0]] = '.'
        dup_tun_map[cur_loc] = '.'
        dup_tun_map[key] = '@'
        # if reachable_keys(tree, dup_tun_map):
        if any(c.islower() for c in dup_tun_map.values()):
            steps_needed += steps_to_remove_keys(tree, dup_tun_map)
        min_steps = min(min_steps, steps_needed)
    return min_steps


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
