import re
from typing import Set

def read_input():
    to_binary = {'F':'0', 'B':'1', 'L':'0', 'R':'1'}
    with open('2020_05.txt') as f:
        boarding_passes = []
        lines = [line.rstrip() for line in f.readlines()]
        for bp in lines:
            boarding_passes.append(int(''.join([to_binary[c] for c in bp]), 2))
        return boarding_passes

def solve_part1(puzzle):
    return max(puzzle)

def solve_part2(puzzle):
    in_order = sorted(puzzle)[1:-1]
    for index, seat in enumerate(in_order):
        if in_order[index + 1] != in_order[index] + 1:
            return in_order[index] + 1
    return -10

puzzle = read_input()
print(sorted(puzzle))
print(f'part 1: {solve_part1(puzzle)}')
print(f'part 2: {solve_part2(puzzle)}')

