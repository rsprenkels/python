def parse_points(instruction):
    p1, p2 = instruction.split(' through ')
    x1, y1 = list(map(int, p1.split(',')))
    x2, y2 = list(map(int, p2.split(',')))
    return x1, y1, x2, y2


class Grid():
    def __init__(self):
        self.grid = [[False] * 1000 for i in range(1000)]
        self.bright = [[0] * 1000 for i in range(1000)]

    def run_instructions(self, instructions):
        for instruction in instructions:
            if instruction.startswith('turn off '):
                x1, y1, x2, y2 = parse_points(instruction[8:])
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        self.grid[y][x] = False
            elif instruction.startswith('turn on '):
                x1, y1, x2, y2 = parse_points(instruction[7:])
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        self.grid[y][x] = True
            else:
                x1, y1, x2, y2 = parse_points(instruction[6:])
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        self.grid[y][x] = not (self.grid[y][x])

        lights_lit = sum([sum([1 for light in row if light]) for row in self.grid])
        return lights_lit

    def run_brightness(self, instructions):
        for instruction in instructions:
            if instruction.startswith('turn off '):
                x1, y1, x2, y2 = parse_points(instruction[8:])
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        self.bright[y][x] = max(self.bright[y][x] - 1, 0)
            elif instruction.startswith('turn on '):
                x1, y1, x2, y2 = parse_points(instruction[7:])
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        self.bright[y][x] += 1
            else:
                x1, y1, x2, y2 = parse_points(instruction[6:])
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        self.bright[y][x] += 2

        lights_brightness = sum([sum(row) for row in self.bright])
        return lights_brightness


def test_1():
    assert Grid().run_instructions(['turn on 0,0 through 999,999']) == 1000000


def test_2():
    assert Grid().run_instructions(['toggle 0,0 through 999,999']) == 1000000


def test_3():
    assert Grid().run_brightness(['toggle 0,0 through 999,999']) == 2000000


if __name__ == '__main__':
    instructions = open('2015_06_input.txt', 'r').readlines()

    print(f"answer 2015_06 part 1: {Grid().run_instructions(instructions)}")

    print(f"answer 2015_06 part 2: {Grid().run_brightness(instructions)}")
