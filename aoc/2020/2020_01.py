number_lines = open('2020_01.txt', 'r').readlines()

numbers = []
for line in number_lines:
    numbers.append(int(line))

for a in range(len(numbers) - 1):
    for b in range(a+1, len(numbers)):
        if numbers[a] + numbers[b] == 2020:
            print(f"2020_01 part 1: {numbers[a] * numbers[b]} ")


for a in range(len(numbers) - 2):
    for b in range(a+1, len(numbers) - 1):
        for c in range(b+1, len(numbers)):
            if numbers[a] + numbers[b] + numbers[c]== 2020:
                print(f"2020_01 part 2: {numbers[a] * numbers[b] * numbers[c]} ")
