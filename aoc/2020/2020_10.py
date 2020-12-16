import copy
from collections import defaultdict
from functools import reduce


def read_input(fname):
    with open(fname) as f:
        return  [int(line.rstrip()) for line in f.readlines()]

def solve_part1(puzzle):
    puzzle = sorted(puzzle)
    device_jolts = max(puzzle) + 3
    puzzle.append(device_jolts)
    diff_counts = defaultdict(int)
    for ndx, x in enumerate(puzzle):
        if ndx == 0:
            diff = x
        else:
            diff = puzzle[ndx] - puzzle[ndx-1]
        diff_counts[diff] += 1
    return diff_counts[1] * diff_counts[3]


reach_count_memento = {0:1}

def reach_count(RT, target):
    if target in reach_count_memento:
        return reach_count_memento[target]
    else:
        result = sum(reach_count(RT, x) for x in RT[target])
        reach_count_memento[target] = result
        return result


def solve_part2(puzzle):
    puzzle.append(0)
    device_jolts = max(puzzle) + 3
    puzzle.append(device_jolts)
    puzzle = sorted(puzzle)
    T = {}
    for ndx, x in enumerate(puzzle):
        T[x] = [elem for elem in puzzle[ndx+1:ndx+4] if elem <= x+3]
    print(puzzle)
    print(T)
    RT = defaultdict(list)
    for k in T:
        for elem in T[k]:
            RT[elem].append(k)
    print(RT)
    return reach_count(RT, device_jolts)

    # paths = 0
    # Q = [(0, set())]
    # while Q:
    #     vertex, seen = Q.pop(0)
    #     if vertex == device_jolts:
    #         paths += 1
    #     else:
    #         seen = copy.copy(seen)
    #         seen.add(vertex)
    #         for adjacent in [a for a in T[vertex] if a not in seen]:
    #             Q.append((adjacent, seen))

# https://www.geeksforgeeks.org/count-possible-paths-two-vertices/
# 19208 for part two for testinput

puzzle = read_input('2020_10.txt')
# puzzle = read_input('2020_10_test.txt')
print(puzzle)
print(f'part 1: {solve_part1(puzzle)}') # 1656
print(f'part 2: {solve_part2(puzzle)}') # 281474976710656 is prob waaay to high, 67706637778944 too
# 981 is too low
# 68719476736 also wrong
