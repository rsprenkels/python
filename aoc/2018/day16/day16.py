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
        self.num_to_opcode = defaultdict(lambda: set(self.opcodes))

    def all_opcodes(self):
        return self.opcodes

    def set_regs(self, A, B, C, D):
        self.regs = [A, B, C, D]

    def exec_num(self, opcode_num, A, B, C):
        return self.exec(next(iter(self.num_to_opcode[opcode_num])), A, B, C)

    def exec(self, opcode, A, B, C):
        self.regs = self.dry_exec(opcode, A, B, C)
        return self.regs

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
    assert cpu.regs == [3, 2, 1, 1]
    assert cpu.exec('addi', 2, 1, 2) == [3, 2, 2, 1]
    assert cpu.regs == [3, 2, 2, 1]


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
        cpu.num_to_opcode[instruction[0]] = matching_opcodes.intersection(cpu.num_to_opcode[instruction[0]])
        index += 4
        if not lines[index].startswith('Before'):
            break
    print(f"day 16 part 1: opcodes more than three: {opcodes_more_than_three}")

    numbers_with_one_opcode = [k for k in cpu.num_to_opcode.keys() if len(cpu.num_to_opcode[k]) == 1]
    while len(numbers_with_one_opcode) < len(cpu.opcodes):
        for is_resolved in numbers_with_one_opcode:
            for k in cpu.num_to_opcode.keys():
                if k != is_resolved:
                    cpu.num_to_opcode[k].discard(next(iter(cpu.num_to_opcode[is_resolved])))
        numbers_with_one_opcode = [k for k in cpu.num_to_opcode.keys() if len(cpu.num_to_opcode[k]) == 1]

    while lines[index] == '\n':
        index += 1

    cpu.set_regs(0, 0, 0, 0)
    for line in lines[index:]:
        print(f"before: {cpu.regs} ", end='')
        instruction = list(map(int, line.split()))
        cpu.exec_num(*instruction)
        print(f"instruction {instruction}  after: {cpu.regs}")
    print(f"day 16 part 2: {cpu.regs[0]}")
