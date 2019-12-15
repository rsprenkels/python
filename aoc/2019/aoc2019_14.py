import math

from namedlist import namedlist

Element = namedlist('Element', ['react', 'needed', 'produced'])


# 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL

def run_reacts(elements, elem, num_needed, rec_depth=1):
    e = elements[elem]
    e.needed += num_needed
    if e.produced < e.needed:
        react = elements[elem].react
        extra_reacts = math.ceil((e.needed - e.produced) / react[0])
        e.produced += extra_reacts * react[0]
        for input_element in react[1].keys():
            if input_element != 'ORE':
                run_reacts(elements, input_element, extra_reacts * react[1][input_element], rec_depth + 1)


def make_fuel(lines, amount=1) -> int:
    elements = {}
    for react_eq in lines:
        reacts, produces = react_eq.split(' => ')
        p_quant, p_elem = produces.split(' ')
        r = (int(p_quant), {p.split(' ')[1]: int(p.split(' ')[0]) for p in reacts.split(', ')})
        elements[p_elem] = Element(r, needed=0, produced=0)
    run_reacts(elements, 'FUEL', amount)
    ore_needed = 0
    for e_with_ore in [elements[e] for e in elements if 'ORE' in elements[e].react[1].keys()]:
        # print(f"{e_with_ore} uses ore")
        num_reacts = math.ceil(e_with_ore.needed / e_with_ore.react[0])
        ore_needed += e_with_ore.react[1]['ORE'] * num_reacts
    return ore_needed


def test_1():
    lines = ['10 ORE => 10 A',
             '1 ORE => 1 B',
             '7 A, 1 B => 1 C',
             '7 A, 1 C => 1 D',
             '7 A, 1 D => 1 E',
             '7 A, 1 E => 1 FUEL', ]

    assert make_fuel(lines) == 31


def test_2():
    lines = [
        '9 ORE => 2 A',
        '8 ORE => 3 B',
        '7 ORE => 5 C',
        '3 A, 4 B => 1 AB',
        '5 B, 7 C => 1 BC',
        '4 C, 1 A => 1 CA',
        '2 AB, 3 BC, 4 CA => 1 FUEL', ]

    assert make_fuel(lines) == 165


def test_3():
    aoc_input = [line.strip() for line in open('aoc2019_14_t1.txt', 'r').readlines()]
    assert make_fuel(aoc_input) == 180697


def fuel_for_ore(aoc_input, total_ore):
    amount = 1
    while make_fuel(aoc_input, amount) < total_ore:
        amount = amount * 2
    s_from, s_to = amount // 2, amount
    while s_from < s_to:
        mid = (s_from + s_to) // 2
        if make_fuel(aoc_input, mid) > total_ore:
            s_to = mid - 1
        else:
            s_from = mid
    return s_from


def test_4():
    aoc_input = [line.strip() for line in open('aoc2019_14_t1.txt', 'r').readlines()]
    ore_amount = 1000000000000
    res = fuel_for_ore(aoc_input, ore_amount)
    assert res == 5586022


def test_part1():
    aoc_input = [line.strip() for line in open('aoc2019_14_input.txt', 'r').readlines()]
    assert make_fuel(aoc_input) == 720484


def test_part2():
    aoc_input = [line.strip() for line in open('aoc2019_14_input.txt', 'r').readlines()]
    assert fuel_for_ore(aoc_input, 1000000000000) == 1993284

if __name__ == '__main__':
    aoc_input = [line.strip() for line in open('aoc2019_14_input.txt', 'r').readlines()]
    print(f"aoc 2019 day 14 part 1 {make_fuel(aoc_input)}")
    print(f"aoc 2019 day 14 part 2 {fuel_for_ore(aoc_input, 1000000000000)}")
