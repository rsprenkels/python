print(sum(len(s[:-1]) - len(eval(s)) for s in open('2015_08_input.txt', 'r')))

# 1346 too high
# 1345 wrong
#
# 1129 too low


STRING = open('2015_08_input.txt').read()
if STRING[-1] == '\n':
    STRING = STRING[:-1]

LINES = STRING.split('\n')

answer1 = 0

for l in LINES:
    answer1 += len(l) - len(eval(l))

print(answer1)
answer2 = 0

for l in LINES:
    answer2 += l.count('\\') + l.count('"') + 2

print(answer2)
