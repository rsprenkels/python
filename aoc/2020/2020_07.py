def read_input():
    with open('2020_07.txt') as f:
        lines =  [line.rstrip().rstrip('.') for line in f.readlines()]
        result = {}
        for line in lines:
            bagtype, contents = line.split(' contain ')
            bagtype = bagtype.rstrip(' bags')
            result[bagtype] = {}
            for bag in  [b.rstrip('s').rstrip(' bag') for b in contents.split(',')]:
                number, *contains_bag = bag.split()
                contains_bag = ' '.join(contains_bag)
                if number != 'no':
                    result[bagtype][contains_bag] = int(number)
        return result

def solve_part1(puzzle):
    bags_reaching_gold = 0
    for start_bag in puzzle.keys():
        Q = [start_bag]
        seen = set()
        found = False
        while Q:
            root = Q.pop()
            for target in puzzle[root]:
                if target in seen:
                    continue
                if target == 'shiny gold':
                    found = True
                    break
                else:
                    seen.add(target)
                    Q.append(target)
        if found:
            bags_reaching_gold += 1
    return bags_reaching_gold

def solve_part2(puzzle):
    bags_needed = 0
    Q = [('shiny gold', 1)]
    while Q:
        bag, multiplier = Q.pop()
        bags_needed += multiplier
        for inner_bag in puzzle[bag]:
            # print(inner_bag, puzzle[bag][inner_bag])
            Q.append((inner_bag, puzzle[bag][inner_bag] * multiplier))
    return bags_needed - 1

puzzle = read_input()
print(puzzle)
print(f'part 1: {solve_part1(puzzle)}')
print(f'part 2: {solve_part2(puzzle)}') # 1039 is too high

