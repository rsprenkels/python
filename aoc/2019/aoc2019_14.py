import math

from namedlist import namedlist

Element = namedlist('Element', ['react', 'needed'])


def run_reacts(elements, elem, num_needed):
    elements[elem].needed += num_needed
    react = elements[elem].react
    for input_element in react[1].keys():
        if input_element != 'ORE':
            run_reacts(elements, input_element, num_needed / react[0] * react[1][input_element])


def make_fuel(lines) -> int:
    elements = {}
    for react_eq in lines:
        reacts, produces = react_eq.split(' => ')
        p_quant, p_elem = produces.split(' ')
        r = (int(p_quant), {p.split(' ')[1]: int(p.split(' ')[0]) for p in reacts.split(', ')})
        elements[p_elem] = Element(r, needed=0)
    run_reacts(elements, 'FUEL', 1)
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


if __name__ == '__main__':
    aoc_input = [line.strip() for line in open('aoc2019_14_input.txt', 'r').readlines()]
    print(make_fuel(aoc_input))
