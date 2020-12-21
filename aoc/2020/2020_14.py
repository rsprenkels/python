import re
from collections import defaultdict


def read_input(file_name):
    with open(file_name) as f:
        return [line.rstrip() for line in f.readlines()]


def solve(puzzle):
    memory = defaultdict(int)
    for instruction in puzzle:
        if instruction[:4] == 'mask':
            _, mask = instruction.split(' = ')
        elif instruction[:3] == 'mem':
            address, value = re.search(r'mem\[(\d+)\] = (\d+)', instruction).groups()
            res = ''.join([bit if mask_bit == 'X' else mask_bit for bit, mask_bit in zip(f'{int(value):0>36b}', mask)])
            memory[int(address)] = int(res, 2)
    return sum(memory[a] for a in memory)

puzzle = read_input('2020_14.txt')
print(puzzle)
print(f'part 1: {solve(puzzle)}')
print(f'part 2: {solve(puzzle)}')

