from aoc import P

# origin: top left
def test_1():
    assert P(10, 15).nesw() == [P(10, 14), P(11, 15), P(10, 16), P(9, 15)]