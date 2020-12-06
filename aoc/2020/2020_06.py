import functools


def read_input():
    with open('2020_06.txt') as f:
        lines =  [line.rstrip() for line in f.readlines()]
        result = []
        while lines:
            group = []
            while lines and lines[0] != '':
                line = lines.pop(0)
                group.append(line)
            result.append(group)
            if lines:
                lines.pop(0)
        return result

def solve_part1(puzzle):
    group_answers = []
    for group in puzzle:
        answers = set()
        for person in group:
            for answer in person:
                answers.add(answer)
        group_answers.append(answers)
    return sum(len(ga) for ga in group_answers)

def solve_part2(puzzle):
    group_answers = []
    for group in puzzle:
        persons_answers = []
        for person in group:
            persons_answers.append({a for a in person})
        one_group = functools.reduce(lambda a, b : a & b, persons_answers)
        group_answers.append(one_group)
    return sum(len(og) for og in group_answers)

puzzle = read_input()
print(puzzle)
print(f'part 1: {solve_part1(puzzle)}') # 7128
print(f'part 2: {solve_part2(puzzle)}') # 3640

