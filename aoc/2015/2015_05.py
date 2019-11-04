lines = open('2015_05_input.txt', 'r').readlines()

# lines = ['ieodomkazucvgmuy']

total_nice = 0

for line in lines:
    still_nice = len([c for c in line if c in "aeiou"]) >= 3
    still_nice = still_nice and len([i for i in range(len(line) - 1) if line[i] == line[i+1]]) > 0
    still_nice = still_nice and len([i for i in range(len(line) - 1) if line[i:i+2] in ['ab', 'cd', 'xy', 'pq']]) == 0
    if still_nice:
        total_nice += 1

print(f"2015_05 part 1 {total_nice}")

new_nice = 0
for line in lines:
    still_nice = False
    for i in range(len(line) - 2):
        if len([x for x in range(i+2, len(line) - 2) if line[i:i+2] == line[x:x+2]]) > 0:
            still_nice = True
            break

    if still_nice:
        still_nice = still_nice and len([i for i in range(len(line) - 2) if line[i] == line[i + 2]]) > 0

    if still_nice:
        new_nice += 1

print(f"2015_05 part 2 {new_nice}")
