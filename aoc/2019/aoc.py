import copy
from collections import namedtuple
from enum import Enum, auto
from typing import List


class P(namedtuple('Point', ['x', 'y'])):
    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    def nesw(self):
        x, y = self.x, self.y
        return [P(x, y-1), P(x+1, y), P(x, y+1), P(x-1, y)]

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
        self.p.extend([0] * 50)  # crude hack for now
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

    def reset_run(self, prog_input=[]):
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
        print(f"{x // 10}", end='')
    print()
    print(f"   ", end='')
    for x in range(x_min, x_max + 1):
        print(f"{x % 10}", end='')
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
