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
        self.p.extend([0] * 100000) # crude hack for now
        self.pc = 0
        self.prog_input = []
        self.output = []
        self.haltcode = Haltcode.NONE
        self.relative_base = 0

    def input(self, data : list):
        self.prog_input.extend(data)

    def decode_next(self):
        instruction = self.p[self.pc]
        self.opcode = instruction % 100
        self.modes = [int(c) for c in f"{instruction // 100:03d}"]
        return self.opcode

    def get(self, pos):
        if self.modes[3 - pos] == 0: # postion mode
            return self.p[self.p[self.pc + pos]]
        elif self.modes[3 - pos] == 1 : # immediate mode
            return self.p[self.pc + pos]
        else: # relative mode
            return self.p[self.p[self.pc + pos] + self.relative_base]

    def set(self, pos, value):
        if self.modes[3 - pos] == 0 : # position mode
            self.p[self.p[self.pc + pos]] = value
        else: # relative mode
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
    tile = [' ', '#', 'o', '_', '*']
    x_min = min([k.x for k in grid.keys()])
    x_max = max([k.x for k in grid.keys()])
    y_min = min([k.y for k in grid.keys()])
    y_max = max([k.y for k in grid.keys()])
    print()
    tile = [' ', '.', '#', 'O']
    for y in range(y_max, y_min - 1, -1):
        for x in range(x_min, x_max + 1):
            if location == P(x, y):
                print('+', end='')
            else:
                print(f"{tile[grid[P(x, y)]]}", end='')
        print()
    print(f"frame:{frame_counter}")

dir_vector = [P(0, 1), P(0, -1), P(-1, 0), P(1, 0)]
dir_cmds = {P(0, 1):[1], P(0, -1):[2], P(-1, 0):[3], P(1, 0):[4]}
back_cmds = {P(0, 1):[2], P(0, -1):[1], P(-1, 0):[4], P(1, 0):[3]}

def breadth_first(grid, location, m):
    unknown_dirs = [dir for dir in dir_vector if grid[location + dir] == 0]
    for dir in unknown_dirs:
        m.input(dir_cmds[dir])
        m.run()
        ret_code = m.output.pop(0)
        if ret_code == 0:
            grid[location + dir] = 2
        elif ret_code == 1:
            grid[location + dir] = 1
            m.input(back_cmds[dir])
            m.run()
            m.output.pop(0)
        else:
            grid[location + dir] = 3
            m.input(back_cmds[dir])
            m.run()
            m.output.pop(0)
            return True
    show_screen(grid, location=location)
    possible_dirs = [dir for dir in unknown_dirs if grid[location + dir] == 1]
    for dir in possible_dirs:
        m.input(dir_cmds[dir])
        m.run()
        ret_code = m.output.pop(0)
        res = breadth_first(grid, location + dir, m)
        m.input(back_cmds[dir])
        m.run()
        ret_code = m.output.pop(0)
        if res:
            return




def part_1(program_file):
    with open(program_file, 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
    m = Machine(instructions)
    m.reset()
    # north (1), south (2), west (3), and east (4)
    grid = defaultdict(int)
    location = P(0, 0)
    grid[location] = 1
    breadth_first(grid, location, m)


def test_part_1():
    res = part_1('aoc2019_15_input.txt')


if __name__ == '__main__':
    res = part_1('aoc2019_15_input.txt')
