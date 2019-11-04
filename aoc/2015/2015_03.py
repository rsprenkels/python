from collections import defaultdict

directions = open('2015_03_input.txt', 'r').readline()
counts = defaultdict(int)

# directions = '^>v<'

location = (0, 0)
counts[location] += 1
for move in directions:
    x, y = location
    if move == '^':
        location = (x, y - 1)
    elif move == 'v':
        location = (x, y + 1)
    elif move == '<':
        location = (x - 1, y)
    elif move == '>':
        location = (x + 1, y)
    counts[location] += 1

print(f"part 1 answer: {len(counts)}")

santa = (0, 0)
robo = (0, 0)
two_counts = defaultdict(int)

two_counts[santa] += 1
two_counts[robo] += 1

for index, move in enumerate(directions):
    if index % 2 == 0:  # santa
        x, y = santa
        if move == '^':
            santa = (x, y - 1)
        elif move == 'v':
            santa = (x, y + 1)
        elif move == '<':
            santa = (x - 1, y)
        elif move == '>':
            santa = (x + 1, y)
        two_counts[santa] += 1
    else:
        x, y = robo
        if move == '^':
            robo = (x, y - 1)
        elif move == 'v':
            robo = (x, y + 1)
        elif move == '<':
            robo = (x - 1, y)
        elif move == '>':
            robo = (x + 1, y)
        two_counts[robo] += 1

print(f"part 2 answer: {len(two_counts)}")
