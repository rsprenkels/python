import aoc


def tunnel_map(lines):
    the_map = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            the_map[P(x, y)] = char
    return the_map


def read_tunnels_fromfile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return tunnel_map(lines)


def test_tm():
    lines = """#########
#b.A.@.a#
#########"""
    tm = tunnel_map(lines)
    assert tm == None