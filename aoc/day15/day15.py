from collections import defaultdict

class Unit:
    def __init__(self, type, location):
        self.type = type
        self.location = location
        self.hitpoints = 200

    def __repr__(self):
        return f"{self.type} {self.location}"

    def set_location(self, location):
        self.location = location


class Board:
    def __init__(self, ascii_lines):
        self.units = set()
        self.walls = {}
        self.width = len(ascii_lines[0])
        self.height = len(ascii_lines)

        for y, line in enumerate(ascii_lines):
            for x, symbol in enumerate(line):
                if symbol == 'G':
                    self.units.add(Unit(symbol, (x, y)))
                elif symbol == 'E':
                    self.units.add(Unit(symbol, (x, y)))
                elif symbol == '#':
                    self.walls[(x, y)] = '#'

    def show(self):
        units = {u.location: u for u in self.units}
        # print(f"type of units is {type(units)}")
        for y in range(self.width):
            for x in range(self.height):
                if (x, y) in [location for location in units]:
                    print(units[(x, y)].type, end='')
                elif (x, y) in self.walls:
                    print('#', end='')
                else:
                    print('.', end='')
            print()

    def is_on_board(self, location):
        x, y = list(location)
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def adjacent(self, location):
        x, y = list(location)
        return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}

    def get_range(self, location):
        return {p for p in self.adjacent(location) if self.is_on_board(p)
                and p not in self.units
                and p not in self.walls}

    def reachable_locations(self, location):
        dm = {}
        self.fill_reachable_locations(dm, location, 1)
        return dm

    def fill_reachable_locations(self, dm, location, step):
        for p in self.get_range(location):
            if p not in dm or step < dm[p]:
                dm[p] = step
                self.fill_reachable_locations(dm, p, step + 1)

    def get_units_in_play_order(self):
        return list(self.units)
        # [self.units[t] for t in sorted(list(self.units.keys()))]

    def round(self):
        play_order = self.get_units_in_play_order()
        for unit in play_order:
            self.play(unit)
        board.show()

    def play(self, unit):
        targets = [u for u in self.get_units_in_play_order() if u.type != unit.type]
        if len(targets) > 0:
            # print(f"unit {unit} targets {targets}")
            if False:  # already next to a target
                pass
            else:  # move
                in_range = set()
                for t in targets:
                    in_range |= self.get_range(t.location)
                # print(f"unit {unit} in_range {in_range}")
                dist_map = self.reachable_locations(unit.location)
                # self.show_dist_map(dist_map)
                if len(dist_map) > 0:
                    min_dist = min({dist_map[p] for p in set(dist_map.keys()).intersection(in_range)})
                    my_var = [p for p in set(dist_map.keys()).intersection(in_range) if dist_map[p] == min_dist]
                    destination = sorted(my_var, key=lambda x: (x[1], x[0]))[0]
                    # print(f"destination {destination}")
                    path_lengths = self.reachable_locations(destination)
                    # self.show_dist_map(path_lengths)
                    tusres = {p for p in set(path_lengths.keys()).intersection(self.adjacent(unit.location))}
                    next_location = sorted(tusres, key=lambda x: (x[1], x[0]))[0]
                    # print(f"unit {unit} destination {destination} next_location {next_location}")
                    unit.set_location(next_location)

    def show_dist_map(self, dm):
        for y in range(self.width):
            for x in range(self.height):
                if (x, y) in dm:
                    print('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[dm[(x, y)]], end='')
                else:
                    print('.', end='')
            print()


test_board = '''\
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
'''

if __name__ == "__main__":
    board = Board(test_board.split())
    board.show()
    for round in range(20):
        board.round()
