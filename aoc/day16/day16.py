import copy
from collections import defaultdict


class Cpu():
    def __init__(self):
        self.regs = []
        self.set_regs(0, 0, 0, 0)
        self.opcodes = ['addr', 'addi', 'mulr', 'muli',
                        'banr', 'bani', 'borr', 'bori',
                        'setr', 'seti', 'gtir', 'gtri',
                        'gtrr', 'eqir', 'eqri', 'eqrr']
        self.num_to_opcode = defaultdict(set)

    def all_opcodes(self):
        return self.opcodes

    def set_regs(self, A, B, C, D):
        self.regs = [A, B, C, D]

    def exec(self, opcode, A, B, C):
        self.regs = self.dry_exec(opcode, A, B, C)

    def dry_exec(self, opcode, A, B, C):
        regs = copy.deepcopy(self.regs)
        if opcode == 'addr':
            regs[C] = self.regs[A] + self.regs[B]
        elif opcode == 'addi':
            regs[C] = self.regs[A] + B
        elif opcode == 'mulr':
            regs[C] = regs[A] * regs[B]
        elif opcode == 'muli':
            regs[C] = regs[A] * B
        elif opcode == 'banr':
            regs[C] = regs[A] & regs[B]
        elif opcode == 'bani':
            regs[C] = regs[A] & B
        elif opcode == 'borr':
            regs[C] = regs[A] | regs[B]
        elif opcode == 'bori':
            regs[C] = regs[A] | B
        elif opcode == 'setr':
            regs[C] = regs[A]
        elif opcode == 'seti':
            regs[C] = A
        elif opcode == 'gtir':
            regs[C] = 1 if A > regs[B] else 0
        elif opcode == 'gtri':
            regs[C] = 1 if regs[A] > B else 0
        elif opcode == 'gtrr':
            regs[C] = 1 if regs[A] > regs[B] else 0
        elif opcode == 'eqir':
            regs[C] = 1 if A == regs[B] else 0
        elif opcode == 'eqri':
            regs[C] = 1 if regs[A] == B else 0
        elif opcode == 'eqrr':
            regs[C] = 1 if regs[A] == regs[B] else 0
        return regs


def test_1():
    cpu = Cpu()
    cpu.set_regs(3, 2, 1, 1)
    assert cpu.dry_exec('addi', 2, 1, 2) == [3, 2, 2, 1]


if __name__ == '__main__':
    lines = open('input.txt', 'r').readlines()
    opcodes_more_than_three = 0
    cpu = Cpu()
    index = 0
    while True:
        before = list(map(int, lines[index][9:-2].split(', ')))
        instruction = list(map(int, lines[index + 1].split()))
        after = list(map(int, lines[index + 2][9:-2].split(', ')))

        cpu.set_regs(*before)
        matching_opcodes = set()
        for opcode in cpu.all_opcodes():
            if after == cpu.dry_exec(opcode, *instruction[1:]):
                matching_opcodes.add(opcode)

        if len(matching_opcodes) >= 3:
            opcodes_more_than_three += 1
        index += 4
        if not lines[index].startswith('Before'):
            break
    print(f"day 16 part 1: opcodes more than three: {opcodes_more_than_three}")
