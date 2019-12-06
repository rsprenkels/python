class OrbitsMap():
    def __init__(self, orbit_map):
        self.orbits_around = {}
        for orbit in orbit_map:
            A, B = orbit.split(')')
            self.orbits_around[B] = A

    def path_to_root(self, node):
        path = {}
        while node in self.orbits_around:
            node = self.orbits_around[node]
            path[node] = len(path) + 1
        return path

    def count_orbits(self):
        return sum([len(self.path_to_root(ob)) for ob in self.orbits_around.keys()])

    def transfers_between(self, A, B) -> int:
        path_A = self.path_to_root(A)
        path_B = self.path_to_root(B)
        traverse = self.orbits_around[B]
        while traverse not in path_A.keys():
            traverse = self.orbits_around[traverse]
        return path_A[traverse] + path_B[traverse] - 2

def test_1():
    lines = [
        'COM)B',
        'B)C',
        'C)D',
        'D)E',
        'E)F',
        'B)G',
        'G)H',
        'D)I',
        'E)J',
        'J)K',
        'K)L',
    ]
    assert OrbitsMap(lines).count_orbits() == 42

def test_2():
    lines = [
        'COM)B',
        'B)C',
        'C)D',
        'D)E',
        'E)F',
        'B)G',
        'G)H',
        'D)I',
        'E)J',
        'J)K',
        'K)L',
        'K)YOU',
        'I)SAN',
    ]
    assert OrbitsMap(lines).transfers_between('YOU', 'SAN') == 4

def test_part1():
    with open('aoc2019_06_input.txt', 'r') as f:
        orbit_map = f.read().splitlines()
    assert OrbitsMap(orbit_map).count_orbits() == 254447

def test_part1_fromreddit():
    with open('aoc2019_06_input.txt', 'r') as f:
        orbit_map = f.read().splitlines()
    assert OrbitsMap(orbit_map).count_orbits() == 254447


def test_part2():
    with open('aoc2019_06_input.txt', 'r') as f:
        orbit_map = f.read().splitlines()
    assert OrbitsMap(orbit_map).transfers_between('YOU', 'SAN') == 445

if __name__ == '__main__':
    with open('aoc2019_06_input.txt', 'r') as f:
        orbit_map = f.read().splitlines()
    print(f"aoc 2019 day 06 part 1 {OrbitsMap(orbit_map).count_orbits()}")
    print(f"aoc 2019 day 06 part 2 {OrbitsMap(orbit_map).transfers_between('YOU','SAN')}")


