from collections import namedtuple
import  math

with open('aoc_day06_input.txt', 'r') as f:
    lines = f.readlines()

minimum_distance = 10000

# minimum_distance = 32
#
# lines = [
# '1, 1',
# '1, 6',
# '8, 3',
# '3, 4',
# '5, 5',
# '8, 9',
# ]

raw_points = [list(map(int, line.split(','))) for line in lines]

Point = namedtuple('Point', 'x y')

points = []
for raw_point in raw_points:
    points.append(Point(raw_point[0], raw_point[1]))

x_min = min(points, key=lambda p : p.x).x
x_max = max(points, key=lambda p : p.x).x
y_min = min(points, key=lambda p : p.y).y
y_max = max(points, key=lambda p : p.y).y

for point in points:
    print(f"{point}")

print(f"I have {len(points)} points")

print(f"x_min {x_min} x_max {x_max}")
print(f"y_min {y_min} y_max {y_max}")

grid = [['.' for y in range(y_max + 1)] for x in range(x_max + 2)]

print(f"len(grid) = {len(grid)}")
print(f"len(grid[0]) = {len(grid[0])}")

def show_grid():
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            point = grid[x][y]
            if (point != None):
                print(f"{grid[x][y]:4}", end='')
            else:
                print('   .', end='')
        print()

# show_grid()

for y in range(len(grid[0])):
    for x in range(len(grid)):
        distances = []
        for index, point in enumerate(points):
            cart_dist = abs(x - point.x) + abs(y - point.y)
            distances.append((index, cart_dist))
        distances = sorted(distances, key=lambda d: d[1])
        # print(f"sorted: {distances}")
        if distances[0][1] != distances[1][1]:
            grid[x][y] = distances[0][0]
        else:
            grid[x][y] = None

infinite_areas = set()
for x in range(len(grid)):
    infinite_areas.add(grid[x][0])
    infinite_areas.add(grid[x][len(grid[0]) - 1])

for y in range(len(grid[0])):
    infinite_areas.add(grid[0][y])
    infinite_areas.add(grid[len(grid) - 1][y])

infinite_areas.remove(None)

show_grid()

print(f"infinite_areas: {infinite_areas}")
areas = set(range(len(points))) - infinite_areas
print(f"areas set is {areas}")

area_sizes = [0 for x in range(len(points))]

for y in range(len(grid[0])):
    for x in range(len(grid)):
        if grid[x][y] is not None:
            area_sizes[grid[x][y]] += 1

area_sizes = list(zip(range(len(points)), area_sizes))

area_sizes = [a for a in area_sizes if a[0] in areas]

area_sizes = sorted(area_sizes, key=lambda s: s[1], reverse=True)

print(f"area_sizes {area_sizes}")
print(f"biggest area is {area_sizes[0][1]}")

# part two: calculate total distance to all points
parttwo_area = 0
for y in range(len(grid[0])):
    for x in range(len(grid)):
        total_distance = 0
        for index, point in enumerate(points):
            cart_dist = abs(x - point.x) + abs(y - point.y)
            total_distance += cart_dist
        if total_distance < minimum_distance:
            grid[x][y] = '#'
            parttwo_area += 1
        else:
            grid[x][y] = '.'

show_grid()

print(f"total parttwo area is {parttwo_area}")