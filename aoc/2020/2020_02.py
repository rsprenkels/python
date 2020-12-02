def read_input():
    with open('2020_02.txt') as f:
        result = []
        for line in f:
            from_to_part, letter_part, pwd = line.split()
            from_to = tuple(map(int, from_to_part.split('-')))
            letter = letter_part[0]
            result.append((from_to, letter, pwd))
        return result


def is_valid_pwd_part1(p):
    ((range_from, range_to), letter, pwd) = p
    occurences = pwd.count(letter)
    return occurences >= range_from and occurences <= range_to


def is_valid_pwd_part2(p):
    (first_second, letter, pwd) = p
    return sum([1 for pos in first_second if pwd[pos - 1] == letter]) == 1


def solve(puzzle, is_valid_pwd):
    return sum([1 for p in puzzle if is_valid_pwd(p)])

puzzle = read_input()
print(f'part 1: {solve(puzzle, is_valid_pwd_part1)}')
print(f'part 2: {solve(puzzle, is_valid_pwd_part2)}')

