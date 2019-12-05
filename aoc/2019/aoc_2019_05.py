import copy

class Machine():
    def __init__(self, program):
        self.program = program
        self.p = None
        self.opcode = None
        self.modes = None

    def reset(self):
        self.p = copy.deepcopy(self.program)
        self.pc = 0

    def decode_next(self):
        instruction = self.p[self.pc]
        self.opcode = instruction % 100
        self.modes = [int(c) for c in f"{instruction // 100:03d}"]
        return self.opcode

    def get(self, pos):
        if self.modes[3 - pos] == 0: # postion mode
            return self.p[self.p[self.pc + pos]]
        else: # immediate mode
            return self.p[self.pc + pos]

    def set(self, pos, value):
        if self.modes[3 - pos] == 0:
            self.p[self.p[self.pc + pos]] = value
        else:
            self.p[self.p[self.pc + pos]] = value

    def inc_pc(self, steps):
        self.pc += steps

    def run(self, prog_input : list):
        self.reset()
        output = []
        while True:
            opcode = self.decode_next()
            # print(f"pc:{self.pc} opcode:{opcode} modes:{self.modes}")
            if opcode == 99:
                return output
            elif opcode == 1: # 1 + 2 -> 3
                self.set(3, self.get(1) + self.get(2))
                self.inc_pc(4)
            elif opcode == 2: # 1 * 2 -> 3
                self.set(3, self.get(1) * self.get(2))
                self.inc_pc(4)
            elif opcode == 3: # input -> 1
                self.set(1, prog_input.pop())
                self.inc_pc(2)
            elif opcode == 4: # 1 -> output
                output.append(self.get(1))
                self.inc_pc(2)
            elif opcode == 5: # jump-if-true
                if self.get(1) != 0:
                    self.pc = self.get(2)
                else:
                    self.inc_pc(3)
            elif opcode == 6: # jump-if-false
                if self.get(1) == 0:
                    self.pc = self.get(2)
                else:
                    self.inc_pc(3)
            elif opcode == 7: # less-than
                if self.get(1) < self.get(2):
                    self.set(3, 1)
                else:
                    self.set(3, 0)
                self.inc_pc(4)
            elif opcode == 8: # equals
                if self.get(1) == self.get(2):
                    self.set(3, 1)
                else:
                    self.set(3, 0)
                self.inc_pc(4)
            else:
                print(f"unknown opcode {opcode}")
                exit(1)

def test_1():
    with open('aoc2019_05_input.txt', 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
        m = Machine(instructions)
        prog_input = [1]
        assert m.run(prog_input) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 9219874]

def test_pos_equal_8():
    m = Machine([3,9,8,9,10,9,4,9,99,-1,8])
    assert m.run([7]) == [0]
    assert m.run([8]) == [1]

def test_pos_less_8():
    m = Machine([3,9,7,9,10,9,4,9,99,-1,8])
    assert m.run([7]) == [1]
    assert m.run([8]) == [0]

def test_pos_jump():
    m = Machine([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
    assert m.run([0]) == [0]
    assert m.run([5]) == [1]

def test_immediate_jump():
    m = Machine([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
    assert m.run([0]) == [0]
    assert m.run([5]) == [1]



if __name__ == '__main__':
    with open('aoc2019_05_input.txt', 'r') as f:
        instructions = list(map(int, f.readline().split(',')))
        m = Machine(instructions)

        print(f"aoc 2019 day 05 part 1 {m.run([1])}")
        print(f"aoc 2019 day 05 part 1 {m.run([5])}")
