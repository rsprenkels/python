def read_input(file_name):
    with open(file_name) as f:
        lines =  [line.rstrip() for line in f.readlines()]
        result = []
        while lines:
            while lines and lines[0] != '':
                line = lines.pop(0)
                result.append(line)
            if lines:
                lines.pop(0)
        return result
    # with open('2020_09.txt') as f:
    #     return  [int(line.rstrip()) for line in f.readlines()]

def solve(puzzle):
    return 1

puzzle = read_input('2020_14.txt')
print(puzzle)
print(f'part 1: {solve(puzzle)}')
print(f'part 2: {solve(puzzle)}')

