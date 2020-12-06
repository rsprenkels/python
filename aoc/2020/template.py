def read_input():
    with open('2020_06.txt') as f:
        lines =  [line.rstrip() for line in f.readlines()]
        result = []
        while lines:
            while lines and lines[0] != '':
                line = lines.pop(0)
                result.append(line)
            if lines:
                lines.pop(0)
        return result

def solve(puzzle):
    return 1

puzzle = read_input()
print(puzzle)
print(f'part 1: {solve(puzzle)}')
print(f'part 2: {solve(puzzle)}')

