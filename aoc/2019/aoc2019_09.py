import copy
import itertools
from enum import Enum, auto
from typing import List


class Haltcode(Enum):
    NONE = auto()
    NEED_INPUT = auto()
    HALTED = auto()


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


def test_part1():
    with open('aoc2019_09_input.txt', 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
    m = Machine(instructions)
    assert m.reset_run([1]) == [4006117640]


def test_part2():
    with open('aoc2019_09_input.txt', 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
    m = Machine(instructions)
    assert m.reset_run([2]) == [88231]


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

def best_amp_array_config(instructions):
    max_output = None
    m = Machine(instructions)
    for index, phase_combi in enumerate(itertools.permutations(list(range(5))), 1):
        io_signal = 0
        for step in range(5):
            io_signal = m.reset_run([phase_combi[step], io_signal])[0]
        max_output = max(io_signal, max_output) if max_output != None else io_signal
    return max_output


def best_amp_array_config_feedbackmode(instructions):
    max_output = None
    m = [Machine(instructions) for _ in range(5)]
    for index, phase_combi in enumerate(itertools.permutations(list(range(5,10))), 1):
        for ndx in range(5):
            m[ndx].reset()
            m[ndx].input([phase_combi[ndx]])
        m[0].input([0])
        while True:
            for step in range(5):
                output = m[step].run()[-1]
                m[(step + 1) % 5].input([output])
            if m[4].haltcode == Haltcode.HALTED:
                break
        io_signal = m[4].output[-1]
        max_output = max(io_signal, max_output) if max_output != None else io_signal
    return max_output


def test_feedback_config_1():
    assert best_amp_array_config_feedbackmode([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                                               27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]) == 139629729


def test_feedback_config_2():
    assert best_amp_array_config_feedbackmode([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
                                               -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
                                               53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]) == 18216


def test_amp_config_1():
    assert best_amp_array_config([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == 43210


def test_amp_config_2():
    assert best_amp_array_config([3,23,3,24,1002,24,10,24,1002,23,-1,23,
                                  101,5,23,23,1,24,23,23,4,23,99,0,0]) == 54321


def test_amp_config_3():
    assert best_amp_array_config([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                                  1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == 65210


if __name__ == '__main__':
    with open('aoc2019_07_input.txt', 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
    print(f"aoc 2019 day 07 part 1 {best_amp_array_config(instructions)}")
    print(f"aoc 2019 day 07 part 2 {best_amp_array_config_feedbackmode(instructions)}")
