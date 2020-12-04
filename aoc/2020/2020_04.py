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

def isEmptySet(s: Set) -> bool:
    return not s

def hasElements(s: Set) -> bool:
    return not not s

def solve_p1(puzzle):
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    valid_pps = 0
    for passport in puzzle:
        if hasElements(required_fields - set(passport.keys())): continue
        valid_pps += 1
    return valid_pps

def between(x: int, a: int, b: int) -> bool:
    return x >= a and x <= b

def solve_p2(puzzle):
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    valid_pps = 0
    for passport in puzzle:
        if hasElements(required_fields - set(passport.keys())): continue
        if not between(int(passport['byr']), 1920, 2002): continue
        if not between(int(passport['iyr']), 2010, 2020): continue
        if not between(int(passport['eyr']), 2020, 2030) or len(passport['eyr']) != 4: continue
        if not re.search(r'^[0-9]+(in|cm)$', passport['hgt']): continue
        height, unit = int(passport['hgt'][:-2]), passport['hgt'][-2:]
        if unit == 'in' and not between(height, 59, 76): continue
        if unit == 'cm' and not between(height, 150, 193): continue
        if not re.search(r'^#[a-f0-9]{6}$', passport['hcl']): continue
        if passport['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']: continue
        if not re.search(r'^[0-9]{9}$', passport['pid']): continue
        valid_pps += 1
    return valid_pps

puzzle = read_input()
print(puzzle)
print(f'part 1: {solve_p1(puzzle)}')
print(f'part 2: {solve_p2(puzzle)}')
# 110 is too high

