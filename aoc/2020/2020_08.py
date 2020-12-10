import copy
from enum import Enum

class Cpu_Status(Enum):
    ENDLESS_LOOP = 1
    PAST_END_OF_MEM = 2

class Computer():
    def __init__(self, path):
        self.mem = []
        self.pc = 0
        self.acc = 0
        with open(path) as f:
            for ndx, line in enumerate(f.readlines()):
                opcode, operand = line.split()
                self.mem.append([opcode, int(operand)])

    def reset(self):
        self.pc = 0

    def clock(self):
        opcode, operand = self.mem[self.pc]
        if opcode == 'nop':
            self.pc += 1
        elif opcode == 'acc':
            self.acc += operand
            self.pc += 1
        elif opcode == 'jmp':
            self.pc += operand

    def run(self, loop_allowed=True) -> int:
        seen = set()
        while (self.pc not in seen or loop_allowed) and self.pc < len(self.mem):
            seen.add(self.pc)
            self.clock()
        if not loop_allowed and self.pc in seen :
            return Cpu_Status.ENDLESS_LOOP
        else:
            return Cpu_Status.PAST_END_OF_MEM


def solve_part1(c: Computer) -> int:
    c.run(loop_allowed=False)
    return c.acc

def solve_part2(c: Computer) -> int:
    for instruction_index in range(len(c.mem)):
        if c.mem[instruction_index][0] in ['nop', 'jmp']:
            new_c = copy.deepcopy(c)
            new_c.mem[instruction_index][0] = {'nop':'jmp', 'jmp':'nop'}[new_c.mem[instruction_index][0]]
            if new_c.run(loop_allowed=False) == Cpu_Status.PAST_END_OF_MEM:
                return new_c.acc
    return None

c = Computer('2020_08.txt')
print(f'part 1: {solve_part1(c)}')
c = Computer('2020_08.txt')
print(f'part 2: {solve_part2(c)}')

