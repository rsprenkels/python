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

def solve(puzzle, reduce_func):
    group_answers = []
    for group in puzzle:
        persons_answers = []
        for person in group:
            persons_answers.append({a for a in person})
        one_group = functools.reduce(reduce_func, persons_answers)
        group_answers.append(one_group)
    return sum(len(og) for og in group_answers)

puzzle = read_input()
print(f'part 1: {solve(puzzle, reduce_func=lambda a, b : a | b)}') # 7128
print(f'part 2: {solve(puzzle, reduce_func=lambda a, b : a & b)}') # 3640
