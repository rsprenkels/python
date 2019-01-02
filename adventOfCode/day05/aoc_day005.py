import string

with open('day05-input.txt', 'r') as f:
    polymer = f.readline()

# polymer = 'dabAcCaCBAcCcaDA'

print(type(polymer), polymer)

poly_list = [c for c in polymer]

class Polymer:
    def __init__(self, poly_list):
        self.poly_list = poly_list

    def get_reduced(self):
        reductions_made = True

        while reductions_made:
            reductions_made = False
            pos = 0
            while pos < len(self.poly_list) - 1:
                c1, c2 = list(self.poly_list[pos:pos+2])
                if c1 != c2 and str.upper(c1) == str.upper(c2):
                    del self.poly_list[pos:pos+2]
                    reductions_made = True
                else:
                    pos += 1
        return self.poly_list

shortest_lenght = len(poly_list)
shortest_char = '_'

for letter in string.ascii_lowercase:
    one_removed = [c for c in poly_list if str.lower(c) != letter]
    poly = Polymer(one_removed)
    poly.get_reduced()
    print(f"letter {letter} gives {len(poly.poly_list)}")
    if len(poly.poly_list) < shortest_lenght:
        shortest_lenght = len(poly.poly_list)
        shortest_char = letter
print(f"shorterst letter {shortest_char} results in {shortest_lenght}")