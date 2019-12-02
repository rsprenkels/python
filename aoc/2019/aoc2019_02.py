import copy

program = list(map(int, open('aoc2019_02_input.txt', 'r').readline().split(',')))

def output_for(p1, p2):
    t = copy.deepcopy(program)
    t[1] = p1
    t[2] = p2
    for pc in range(0, len(t), 4):
        if t[pc] == 99:
            break
        elif t[pc] == 1:
            t[t[pc + 3]] = t[t[pc + 1]] + t[t[pc + 2]]
        elif t[pc] == 2:
            t[t[pc + 3]] = t[t[pc + 1]] * t[t[pc + 2]]
        else:
            print("unknown instruction")
            exit(1)
    return t[0]

print(f"aoc 2019 day 02 part 1 {output_for(12, 2)}")

for noun in range(100):
    for verb in range(100):
        if output_for(noun, verb) == 19690720:
            print(f"aoc 2019 day 02 part 2 {100 * noun + verb}")
            exit()
print("no solution found")

