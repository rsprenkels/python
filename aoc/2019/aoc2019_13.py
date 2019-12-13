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


def part_1(program_file):
    with open(program_file, 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
    m = Machine(instructions)
    m.reset()
    grid = defaultdict(int)
    while m.haltcode != Haltcode.HALTED:
        m.run()
    while m.output:
        x = m.output.pop(0)
        y = m.output.pop(0)
        grid[(P(x, y))] = m.output.pop(0)
    return grid


def show_screen(grid, frame_counter=0):
    tile = [' ', '#', 'o', '_', '*']
    x_min = min([k.x for k in grid.keys()])
    x_max = max([k.x for k in grid.keys()])
    y_min = min([k.y for k in grid.keys()])
    y_max = max([k.y for k in grid.keys()])
    print()
    tile = [' ', '#', '@', '_', 'O']
    for y in range(y_max, y_min - 1, -1):
        for x in range(max(0, x_min), x_max + 1):
            print(f"\033[{y};{x}H{tile[grid[(x, y)]]}", end='')
        print()
    # print(f"frame:{frame_counter} score:{grid[(-1, 0)]}")


def test_part1():
    res = part_1('aoc2019_13_input.txt')
    show_screen(res)
    num_blocks = len([g for g in res.keys() if res[g] == 2])
    assert num_blocks == 265



def part_2(program_file):
    with open(program_file, 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
    m = Machine(instructions)
    m.program[0] = 2
    m.reset()
    the_input=[0,1,]
    frame_counter = 0
    grid = defaultdict(int)
    while m.haltcode != Haltcode.HALTED:
        m.run()
        frame_counter += 1
        while m.output:
            x = m.output.pop(0)
            y = m.output.pop(0)
            grid[(P(x, y))] = m.output.pop(0)
        show_screen(grid, frame_counter)
        paddle = [k for k in grid.keys() if grid[k] == 3][0]
        ball = [k for k in grid.keys() if grid[k] == 4][0]
        if paddle.x < ball.x:
            m.input([1])
        elif paddle.x > ball.x:
            m.input([-1])
        else:
            m.input([0])


def test_part2():
    res = part_2('aoc2019_13_input.txt')


def test_day9_features_1():
    m = Machine([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
    assert m.reset_run([]) == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

def test_day9_features_2():
    m = Machine([1102,34915192,34915192,7,4,7,99,0])
    assert m.reset_run([]) == [1219070632396864]

def test_day9_features_3():
    m = Machine([104,1125899906842624,99])
    assert m.reset_run([]) == [1125899906842624]

def test_pos_equal_8():
    m = Machine([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
    assert m.reset_run([7]) == [0]
    assert m.reset_run([8]) == [1]

def test_pos_less_8():
    m = Machine([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
    assert m.reset_run([7]) == [1]
    assert m.reset_run([8]) == [0]

def test_pos_jump():
    m = Machine([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
    assert m.reset_run([0]) == [0]
    assert m.reset_run([5]) == [1]

def test_immediate_jump():
    m = Machine([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
    assert m.reset_run([0]) == [0]
    assert m.reset_run([5]) == [1]

if __name__ == '__main__':
    res = part_2('aoc2019_13_input.txt')
