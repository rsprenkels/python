from collections import namedtuple

with open('patches.txt', 'r') as f:
    patches = f.read().splitlines()

Patch = namedtuple('Patch', 'id x y w h')

patch_w, patch_h = (1000,1000)

# patches = [
#     '#1 @ 1,3: 4x4',
#     '#2 @ 3,1: 4x4',
#     '#3 @ 5,5: 2x2',
# ]
#
# patch_w, patch_h = (10,10)

class Fabric ():

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.squares = []
        self.patches = []
        for row in range(self.height):
            self.squares.append([None for col in range(self.width)])
        for row in range(self.height):
            for col in range(self.width):
                self.squares[row][col] = 0

    def add_patch(self, patch):
        id,_,origin,dimensions = patch.split()
        patch_x, patch_y = list(map(int,origin[:-1].split(',')))
        patch_w, patch_h = list(map(int,dimensions.split('x')))
        id = int(id[1:])
        patch = Patch(id,patch_x, patch_y, patch_w, patch_h)
        print(f"adding patch at {patch.x},{patch.y} of {patch.w}x{patch.h}")
        for row in range(patch.x, patch.x + patch.w):
            for col in range(patch.y, patch.y + patch.h):
                self.squares[row][col] += 1
        self.patches.append(patch)

    def get_overallocated_cells(self):
        count = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.squares[row][col] > 1:
                    count += 1
        return count

    def get_clear_patch(self):
        for patch in self.patches:
            found_in_double_use = False
            for row in range(patch.x, patch.x + patch.w):
                for col in range(patch.y, patch.y + patch.h):
                    if self.squares[row][col] > 1:
                        found_in_double_use = True
                        break
                if found_in_double_use:
                    break
            if not found_in_double_use:
                return patch
        return None

    def __str__(self):
        out = ''
        for row in range(self.height):
            for col in range(self.width):
                val = self.squares[row][col]
                if val == 0:
                    out += '.'
                else:
                    out += str(val)
            out += '\n'
        for patch in self.patches:
            out += f"{patch}\n"
        return out

fabric = Fabric(width=patch_w,height=patch_h)

print(fabric)

for patch in patches:
    fabric.add_patch(patch)

print(fabric)

print(f"I see {fabric.get_overallocated_cells()} overallocated cells")
print(f"patch {fabric.get_clear_patch()} is clear")