from collections import defaultdict

class Unit:
    def __init__(self, type, location):
        self.type = type
        self.location = location
        self.hitpoints = 200
        self.attack_value = 3

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
        self.round_counter = 0

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
        print(f"R{self.round_counter:4}  ", end='')
        for y in range(self.height):
            if y > 0:
                print("       ", end='')
            for x in range(self.width):
                if (x, y) in [location for location in units]:
                    print(units[(x, y)].type, end='')
                elif (x, y) in self.walls:
                    print('#', end='')
                else:
                    print('.', end='')
            for loc in [u.location for u in self.get_units_in_play_order()]:
                if loc[1] == y:
                    print(f" {units[loc].type}({units[loc].hitpoints}) ", end='')
            print()

    def is_on_board(self, location):
        x, y = list(location)
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def adjacent(self, location):
        x, y = list(location)
        return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}

    def get_range(self, location):
        return {p for p in self.adjacent(location) if self.is_on_board(p)
                and p not in {u.location for u in self.units}
                and p not in self.walls}

    def reachable_locations(self, location, include_location = False):
        dm = {}
        if include_location:
            dm[location] = 0
        self.fill_reachable_locations(dm, location, 1)
        return dm

    def fill_reachable_locations(self, dm, location, step):
        for p in self.get_range(location):
            if p not in dm or step < dm[p]:
                dm[p] = step
                self.fill_reachable_locations(dm, p, step + 1)

    def get_units_in_play_order(self):
        return sorted(list(self.units), key=lambda u: (u.location[1], u.location[0]))
        # [self.units[t] for t in sorted(list(self.units.keys()))]

    def get_units_by_locations(self, locations):
        return sorted([u for u in self.units if u.location in locations], key=lambda u: (u.location[1], u.location[0]))

    def round(self):
        play_order = self.get_units_in_play_order()
        self.sum_hitpoints = sum([u.hitpoints for u in self.units])
        did_something = False
        for unit in play_order:
            did_something |= self.play(unit)
        if did_something:
            self.round_counter += 1
            board.show()
        else:
            print(f"last round was {self.round_counter - 1} sum_hp {self.sum_hitpoints} game result {(self.round_counter - 1) * self.sum_hitpoints}")
            for u in self.units:
                print(f"{u} {u.hitpoints}")
        return did_something

    def play(self, unit):
        if unit not in self.units:
            return False
        assert unit.hitpoints > 0
        # print(f"play {unit} ", end='')
        targets = [u for u in self.get_units_in_play_order() if u.type != unit.type]
        target_locations = {u.location for u in targets}
        did_something = False
        if len(targets) > 0:
            # print(f"unit {unit} targets {targets}")
            adjacent_target_locations = [u for u in target_locations.intersection(self.adjacent(unit.location))]
            if len(adjacent_target_locations) > 0:  # already next to target(s)
                targets = self.get_units_by_locations(adjacent_target_locations)
                min_hitpoints = min([u.hitpoints for u in targets])
                to_attack = [t for t in targets if t.hitpoints == min_hitpoints][0]
                if to_attack.location == (4,2) and to_attack.type == 'E':
                    print(f"{unit} attacks {to_attack} from {to_attack.hitpoints}")
                to_attack.hitpoints -= unit.attack_value
                if to_attack.hitpoints <= 0:
                    self.remove(to_attack)
                    # print (f"killed {to_attack}")
                did_something = True
                # print(f"{unit} already has a target")
            else:  # move
                in_range = set()
                for t in targets:
                    in_range |= self.get_range(t.location)
                # print(f"unit {unit} in_range {in_range}")
                if len(in_range) > 0: # there are targets that have open adjacent squares
                    dist_map = self.reachable_locations(unit.location)
                    # self.show_dist_map(dist_map)
                    if len(dist_map) > 0:
                        dist_per_range = {dist_map[p] for p in set(dist_map.keys()).intersection(in_range)}
                        if len(dist_per_range) > 0:
                            min_dist = min(dist_per_range)
                            my_var = [p for p in set(dist_map.keys()).intersection(in_range) if dist_map[p] == min_dist]
                            destination = sorted(my_var, key=lambda x: (x[1], x[0]))[0]
                            # print(f"destination {destination}")
                            path_lengths = self.reachable_locations(destination, include_location=True)
                            # self.show_dist_map(path_lengths)
                            tusres = {p:path_lengths[p] for p in set(path_lengths.keys()).intersection(self.get_range(unit.location))}
                            shortest_path = min([tusres[k] for k in tusres])
                            tusres = {loc for loc in tusres if tusres[loc] == shortest_path}
                            next_location = sorted(tusres, key=lambda x: (x[1], x[0]))[0]
                            # print(f"unit {unit} destination {destination} next_location {next_location}")
                            unit.set_location(next_location)
                            # print(f"to {next_location}")
                            did_something = True
                        else:
                            pass
        return did_something

    def show_dist_map(self, dm):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in dm:
                    print('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[dm[(x, y)]], end='')
                else:
                    print('.', end='')
            print()

    def remove(self, unit):
        self.units.remove(unit)


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


# test_board = '''\
# #########
# #GG..G..#
# #G..E..G#
# #.......#
# #.......#
# #G..G..G#
# #.......#
# #.......#
# #########
# '''

#
# test_board = '''\
# #########
# #...GGG.#
# #..GE...#
# #G.GG...#
# #G......#
# #.......#
# #.......#
# #.......#
# #########
# '''

test_board = '''\
#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######   
'''


if __name__ == "__main__":
    board = Board(test_board.split())
    board.show()
    keep_playing = True
    while keep_playing:
        keep_playing = board.round()
