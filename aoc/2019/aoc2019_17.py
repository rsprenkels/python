import copy
import itertools
import math
import sys
from collections import defaultdict, namedtuple
from enum import Enum, auto
from typing import List


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


class Haltcode(Enum):
    NONE = auto()
    NEED_INPUT = auto()
    HALTED = auto()
    RUNNING = auto()


class Machine():
    def __init__(self, program: List[int]):
        self.program = program
        self.p = None
        self.opcode = None
        self.modes = None
        self.relative_base = 0
        self.haltcode = Haltcode.NONE
        self.reset()

    def reset(self):
        self.p = copy.deepcopy(self.program)
        self.p.extend([0] * 100000)  # crude hack for now
        self.pc = 0
        self.prog_input = []
        self.output = []
        self.haltcode = Haltcode.NONE
        self.relative_base = 0

    def input(self, data: list):
        self.prog_input.extend(data)

    def decode_next(self):
        instruction = self.p[self.pc]
        self.opcode = instruction % 100
        self.modes = [int(c) for c in f"{instruction // 100:03d}"]
        return self.opcode

    def get(self, pos):
        if self.modes[3 - pos] == 0:  # postion mode
            return self.p[self.p[self.pc + pos]]
        elif self.modes[3 - pos] == 1:  # immediate mode
            return self.p[self.pc + pos]
        else:  # relative mode
            return self.p[self.p[self.pc + pos] + self.relative_base]

    def set(self, pos, value):
        if self.modes[3 - pos] == 0:  # position mode
            self.p[self.p[self.pc + pos]] = value
        else:  # relative mode
            self.p[self.p[self.pc + pos] + self.relative_base] = value

    def inc_pc(self, steps):
        self.pc += steps

    def reset_run(self, prog_input: list):
        self.reset()
        self.input(prog_input)
        return self.run()

    def run(self):
        self.haltcode = Haltcode.RUNNING
        while True:
            opcode = self.decode_next()
            # print(f"pc:{self.pc} opcode:{opcode} modes:{self.modes}")
            if opcode == 99:
                self.haltcode = Haltcode.HALTED
                return self.output
            elif opcode == 1:  # 1 + 2 -> 3
                self.set(3, self.get(1) + self.get(2))
                self.inc_pc(4)
            elif opcode == 2:  # 1 * 2 -> 3
                self.set(3, self.get(1) * self.get(2))
                self.inc_pc(4)
            elif opcode == 3:  # input -> 1
                if self.prog_input:
                    self.set(1, self.prog_input.pop(0))
                    self.inc_pc(2)
                else:
                    self.haltcode = Haltcode.NEED_INPUT
                    return self.output
            elif opcode == 4:  # 1 -> output
                self.output.append(self.get(1))
                self.inc_pc(2)
            elif opcode == 5:  # jump-if-true
                if self.get(1) != 0:
                    self.pc = self.get(2)
                else:
                    self.inc_pc(3)
            elif opcode == 6:  # jump-if-false
                if self.get(1) == 0:
                    self.pc = self.get(2)
                else:
                    self.inc_pc(3)
            elif opcode == 7:  # less-than
                self.set(3, 1 if self.get(1) < self.get(2) else 0)
                self.inc_pc(4)
            elif opcode == 8:  # equals
                self.set(3, 1 if self.get(1) == self.get(2) else 0)
                self.inc_pc(4)
            elif opcode == 9:  # adjust relative base
                self.relative_base += self.get(1)
                self.inc_pc(2)
            else:
                print(f"unknown opcode {opcode}")
                exit(1)


def show_screen(grid, frame_counter=0, location=None):
    x_min = min([k.x for k in grid.keys()])
    x_max = max([k.x for k in grid.keys()])
    y_min = min([k.y for k in grid.keys()])
    y_max = max([k.y for k in grid.keys()])
    print()
    print(f"   ", end='')
    for x in range(x_min, x_max + 1):
        print(f"{x//10}", end='')
    print()
    print(f"   ", end='')
    for x in range(x_min, x_max + 1):
        print(f"{x%10}", end='')
    print()
    for y in range(y_max, y_min - 1, -1):
        print(f"{y:2} ", end='')
        for x in range(x_min, x_max + 1):
            if P(x, y) in grid:
                print(f"{grid[P(x, y)]}", end='')
            else:
                print(' ', end='')
        print()
    print(f"frame:{frame_counter} x {x_min} {x_max}  y {y_min} {y_max}")


dir_vector = [P(0, 1), P(0, -1), P(-1, 0), P(1, 0)]
turn_right = [P(1, 0), P(0, 1), P(0, -1), P(-1, 0), ]
dir_cmds = {P(0, 1): [1], P(0, -1): [2], P(-1, 0): [3], P(1, 0): [4]}
back_cmds = {P(0, 1): [2], P(0, -1): [1], P(-1, 0): [4], P(1, 0): [3]}


def part_1(program_file):
    with open(program_file, 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
    m = Machine(instructions)
    m.reset()
    # north (1), south (2), west (3), and east (4)
    grid = {}
    loc = P(0, 0)
    m.run()
    while m.output:
        c = m.output.pop(0)
        if c in [35, 46, 60, 62, 118, 94]:
            grid[loc] = {35: '#', 46: '.', 60: '<', 62: '>', 118: 'v', 94: '^'}[c]
            loc += dir_vector[3]
        elif c == 10:
            loc = P(0, loc.y + 1)
        else:
            pass
    # show_screen(grid)
    intersects = [k for k in grid.keys() if grid[k] == '#' and all([k + v in grid.keys() for v in dir_vector]) and all(
        [grid[k + v] == '#' for v in dir_vector])]
    sum_align = sum([p.x * p.y for p in intersects])
    return sum_align, grid


def test_part_1():
    res, grid = part_1('aoc2019_17_input.txt')
    assert res == 10632


sym_to_dir = {'^': P(0, 1), 'v': P(0, -1), '<': P(-1, 0), '>': P(1, 0)}


# dir_vector = [P(0, 1), P(0, -1), P(-1, 0), P(1, 0)]

def on_scaffold(grid, loc):
    return loc in grid.keys() and grid[loc] == '#'


def part_2(program_file):
    res, grid = part_1('aoc2019_17_input.txt')
    show_screen(grid)
    loc = [k for k in grid.keys() if grid[k] in ['<', '>', 'v', '^']][0]
    dir = sym_to_dir[grid[loc]]
    moves = []
    while on_scaffold(grid, loc + dir) or on_scaffold(grid, loc + dir.right()) or on_scaffold(grid, loc + dir.left()):
        steps = 0
        while on_scaffold(grid, loc + dir):
            loc += dir
            steps += 1
        if steps:
            moves.append(str(steps))
        if on_scaffold(grid, loc + dir.left()):
            moves.append('L')
            dir = dir.left()
        elif on_scaffold(grid, loc + dir.right()):
            moves.append('R')
            dir = dir.right()
    codebook = defaultdict(int)
    for code_len in range(2, len(moves) // 2 + 1):
        # print(f"tot:{len(moves)} len:{code_len:3}")
        for start_index in range(len(moves) - code_len):
            code = tuple(moves[start_index:start_index + code_len])
            codebook[code] += 1
    return codebook

def test_part_2():
    res = part_2('aoc2019_17_input.txt')
    print()
    print(f"book has {len(res)} codes")
    print('\n'.join(str(x) for x in
                    sorted([(k, res[k], (len(k) - 1) * res[k]) for index, k in enumerate(res.keys()) if res[k] > 1],
                           key=lambda x: -x[2])))

# if __name__ == '__main__':
#     res_1 = part_1('aoc2019_15_input.txt')
#     print(f"aoc 2019 day 15 part 1: {res_1}")
