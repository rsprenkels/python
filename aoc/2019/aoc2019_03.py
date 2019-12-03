def path_to_points(path):
    px, py = 0, 0
    points = set()
    for step in path:
        direction = step[0]
        distance = int(step[1:])
        if direction == 'U':
            for y in range(distance):
                py += 1
                points.add((px, py))
        elif direction == 'D':
            for y in range(distance):
                py -= 1
                points.add((px, py))
        elif direction == 'R':
            for x in range(distance):
                px += 1
                points.add((px, py))
        else: # 'L'
            for x in range(distance):
                px -= 1
                points.add((px, py))
    points.discard((0,0))
    return points


def intersect_distance(wire_1, wire_2):
    w1 = path_to_points(wire_1)
    w2 = path_to_points(wire_2)
    return min([abs(p[0]) + abs(p[1]) for p in w1.intersection(w2)])


def test_1():
    wire_1 = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']
    wire_2 = ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83',]
    assert intersect_distance(wire_1, wire_2) == 159


if __name__ == '__main__':
    with open('aoc2019_03_input.txt', 'r') as f:
        wires = [line.split(',') for line in f.readlines()]
    print(f"aoc 2019 day 03 part 1 {intersect_distance(*wires)}")
