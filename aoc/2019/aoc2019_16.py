import math
from functools import reduce


def fft(signal, num_phases):
    pattern = [0, 1, 0, -1]
    sig_int = [int(c) for c in signal]
    for phase in range(1, num_phases + 1):
        new_val = []
        for digit in range(len(signal)):
            act_pattern = reduce(lambda x, y: x + y, [[e] * (digit + 1) for e in pattern]) * (
                    1 + math.ceil(len(signal) / ((digit + 1) * 4)))
            x = sum([t[0] * t[1] for t in zip(sig_int, act_pattern[1:])])
            new_val.append(abs(x) % 10)
        sig_int = new_val
    return ''.join([str(d) for d in sig_int])


def test_1():
    assert fft('12345678', 1) == '48226158'
    assert fft('12345678', 2) == '34040438'


def test_2():
    assert fft('80871224585914546619083218645595', 100)[:8] == '24176176'


def test_part1():
    with open('aoc2019_16_input.txt', 'r') as f:
        signal = f.readline()
    assert fft(signal, 100)[:8] == '11833188'


def test_part2():
    with open('aoc2019_16_input.txt', 'r') as f:
        signal = f.readline()
    offset = int(signal[:7])
    assert fft(signal * 10000, 100)[offset:offset + 8] == '11833188'


if __name__ == '__main__':
    with open('aoc2019_16_input.txt', 'r') as f:
        signal = f.readline()
    # print(f"aoc 2019 day 07 part 1 {best_amp_array_config(instructions)}")
