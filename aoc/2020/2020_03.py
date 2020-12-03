def read_input():
    with open('2020_03.txt') as f:
        return [list(line.rstrip()) for line in f.readlines()]

def solve(puzzle, right=3, down=1):
    map_bottom = len(puzzle)
    width = len(puzzle[0])
    trees = 0
    for y in range(0, map_bottom, down):
        if puzzle[y][(y * right) % width] == '#':
            trees += 1
    return trees

puzzle = read_input()
print(f'part 1: {solve(puzzle, 3, 1)}')
print(f'part 2: {solve(puzzle, 1, 1) * solve(puzzle, 3, 1) * solve(puzzle, 5, 1) * solve(puzzle, 7, 1) * solve(puzzle, 1, 2)}')

# goal: count how many trees there are on a given slope, to reach bottom line. Start is at (0,0), top left of the forest

# sample of the input file

# ..#......###....#...##..#.#....
# .#.#.....#.##.....###...##...##
# ..#.#..#...........#.#..#......
# ..#......#..........###........
# ...#..###..##.#..#.......##..##
# ......#.#.##...#...#....###....
# ..........##.....##..##......#.
# ......#...........#............
# #....#..........#..............
# .#........##.............###.##




