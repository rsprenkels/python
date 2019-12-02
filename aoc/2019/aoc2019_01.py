import math

lines = open('aoc2019_01_input.txt', 'r').readlines()

modules = [int(m) for m in lines]

total_fuel = sum([math.floor(m / 3) - 2 for m in modules])

print(f"aoc 2019 day 01 part 1 {total_fuel}")

def fuel_for(mass):
    return max(math.floor(mass / 3) - 2, 0)

fuel_part2 = 0
for m in modules:
    module_fuel = fuel_for(m)
    fuel_part2 += module_fuel
    additional_fuel = fuel_for(module_fuel)
    while additional_fuel > 0:
        fuel_part2 += additional_fuel
        additional_fuel = fuel_for(additional_fuel)
print(f"aoc 2019 day 01 part 2 {fuel_part2}")