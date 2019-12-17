from itertools import accumulate

x = open('aoc2019_16_input.txt').read()
x = list(map(int, (x * 10000)[int(x[:7]):][::-1]))

for _ in range(100):
    x = list(accumulate(x, lambda a, b: (a + b) % 10))

print(*x[::-1][:8], sep='')
