

with open('2015_08_input.txt', 'r') as f:
    diff = 0
    for line in f.readlines():
        line = line.rstrip()
        diff += len(line) - len(eval(line))
    print(f'answer part 1 = {diff}')
    #1342


with open('2015_08_input.txt', 'r') as f:
    diff = 0
    for line in f.readlines():
        line = line.rstrip()
        diff += 2
        for c in line:
            if c == '\\':
                diff += 1
            elif c == '"':
                diff += 1
            else:
                diff += 0
    print(f'answer part 2 = {diff}')
    # 2074