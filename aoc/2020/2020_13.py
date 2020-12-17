def read_input(fname: str):
    with open(fname) as f:
        depart = int(f.readline())
        times = f.readline().split(',')
        return (depart, times)

def solve(puzzle):
    depart, times = puzzle
    busses = [int(b) for b in times if b != 'x']
    print(f'busses {busses}')
    earliest_bus = None
    for bus in busses:
        if depart % bus == 0:
            wait_time = 0
        else:
            wait_time = bus - (depart % bus)
        if earliest_bus == None or earliest_bus[0] > wait_time:
            earliest_bus = (wait_time, bus)
    return earliest_bus[0] * earliest_bus[1]

puzzle = read_input('2020_13.txt')
print(puzzle)
print(f'part 1: {solve(puzzle)}')
print(f'part 2: {solve(puzzle)}')

