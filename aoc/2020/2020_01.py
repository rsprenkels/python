
number_lines = open('2020_01.txt', 'r').readlines()

numbers = []
for line in number_lines:
    numbers.append(int(line))

for a in range(len(numbers) - 1):
    for b in range(a+1, len(numbers)):
        if numbers[a] + numbers[b] == 2020:
            print(f"2020_01 part 1: {numbers[a] * numbers[b]} ")


for a in range(len(numbers) - 2):
    for b in range(a+1, len(numbers) - 1):
        for c in range(b+1, len(numbers)):
            if numbers[a] + numbers[b] + numbers[c]== 2020:
                print(f"2020_01 part 2: {numbers[a] * numbers[b] * numbers[c]} ")


import math
from itertools import combinations

def read_input():
    with open('2020_01.txt') as f:
        return [int(line) for line in f]

def solve(puzzle, n):
    for c in combinations(puzzle, n):
        if sum(c) != 2020: continue
        return math.prod(c)

puzzle = read_input()
print(f'part 1: {solve(puzzle, 2)}')
print(f'part 2: {solve(puzzle, 3)}')
