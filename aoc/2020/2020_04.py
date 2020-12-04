import re
from typing import Set

def read_input():
    with open('2020_04.txt') as f:
        passport_list = []
        lines =  [line.rstrip() for line in f.readlines()]
        while lines:
            passport = {}
            while lines and lines[0] != '':
                for kv_list in  [kv.split(':') for kv in lines.pop(0).split()]:
                    k, v = kv_list
                    passport[k] = v
            passport_list.append(passport)
            if lines:
                lines.pop(0)
        return passport_list

def hasElements(s: Set) -> bool:
    return not not s

def between(x: int, a: int, b: int) -> bool:
    return x >= a and x <= b

def isvalid_part1(passport) -> bool:
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    if hasElements(required_fields - set(passport.keys())): return False
    return True

def isvalid_part2(passport) -> bool:
    if not isvalid_part1(passport): return False
    if not between(int(passport['byr']), 1920, 2002): return False
    if not between(int(passport['iyr']), 2010, 2020): return False
    if not between(int(passport['eyr']), 2020, 2030) or len(passport['eyr']) != 4: return False
    if not re.search(r'^[0-9]+(in|cm)$', passport['hgt']): return False
    height, unit = int(passport['hgt'][:-2]), passport['hgt'][-2:]
    if unit == 'in' and not between(height, 59, 76): return False
    if unit == 'cm' and not between(height, 150, 193): return False
    if not re.search(r'^#[a-f0-9]{6}$', passport['hcl']): return False
    if passport['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']: return False
    if not re.search(r'^[0-9]{9}$', passport['pid']): return False
    return True

def solve(puzzle, tester=isvalid_part1):
    return len([1 for passport in puzzle if tester(passport)])

puzzle = read_input()
print(f'part 1: {solve(puzzle)}')
print(f'part 2: {solve(puzzle, isvalid_part2)}')

