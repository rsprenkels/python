import sys
from collections import defaultdict


def path_to_points(path):
    px, py = 0, 0
    points = defaultdict(lambda: int(sys.maxsize))
    stepcount = 0
    for step in path:
        direction = step[0]
        distance = int(step[1:])
        if direction == 'U':
            for y in range(distance):
                stepcount += 1
                py += 1
                points[(px, py)] = min (points[(px, py)], stepcount)
        elif direction == 'D':
            for y in range(distance):
                stepcount += 1
                py -= 1
                points[(px, py)] = min (points[(px, py)], stepcount)
        elif direction == 'R':
            for x in range(distance):
                stepcount += 1
                px += 1
                points[(px, py)] = min (points[(px, py)], stepcount)
        else: # 'L'
            for x in range(distance):
                stepcount += 1
                px -= 1
                points[(px, py)] = min (points[(px, py)], stepcount)
    points.pop((0,0), None)
    return points


def intersect_distance(wire_1, wire_2):
    w1 = set(path_to_points(wire_1).keys())
    w2 = set(path_to_points(wire_2).keys())
    return min([abs(p[0]) + abs(p[1]) for p in w1.intersection(w2)])


def minimum_delay(wire_1, wire_2):
    w1 = path_to_points(wire_1)
    w2 = path_to_points(wire_2)
    keys_w1 = set(w1.keys())
    keys_w2 = set(w2.keys())
    return min([(w1[p] + w2[p]) for p in keys_w1.intersection(keys_w2)])


def test_1():
    wire_1 = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']
    wire_2 = ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83',]
    assert intersect_distance(wire_1, wire_2) == 159


def test_delay():
    wire_1 = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']
    wire_2 = ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83',]
    assert minimum_delay(wire_1, wire_2) == 610


if __name__ == '__main__':
    with open('aoc2019_03_input.txt', 'r') as f:
        wires = [line.split(',') for line in f.readlines()]
    print(f"aoc 2019 day 03 part 1 {intersect_distance(*wires)}")
    print(f"aoc 2019 day 03 part 2 {minimum_delay(*wires)}")
