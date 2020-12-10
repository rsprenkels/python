from itertools import combinations

def read_input():
    with open('2020_09.txt') as f:
        return  [int(line.rstrip()) for line in f.readlines()]

def solve_part1(puzzle, pa=25):
    for ndx in range(pa, len(puzzle)):
        found = False
        for a, b in combinations(puzzle[ndx-pa:ndx], 2):
            if a + b == puzzle[ndx]:
                found = True
                break
        if not found:
            return puzzle[ndx]

def solve_part2(puzzle, p1):
    for a, b in combinations(range(len(puzzle)), 2):
        if sum(puzzle[a:b]) == p1:
            return (min(puzzle[a:b]) + max(puzzle[a:b]))
    return None

puzzle = read_input()
p1 = solve_part1(puzzle)
print(f'part 1: {p1}')
print(f'part 2: {solve_part2(puzzle, p1)}')

