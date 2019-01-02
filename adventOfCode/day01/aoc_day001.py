offsets = open('input.txt', 'r').readlines()

deltas = list(map(int, offsets))
total_offset = sum(deltas)

print(f"end frequency is {total_offset}")

found_seen_twice = False

frequencies_seen = set()

cur_frequency = 0

while not found_seen_twice:
    for delta in deltas:
        cur_frequency += delta
        if cur_frequency in frequencies_seen:
            print(f"seeing frequency {cur_frequency} for second time, checked {len(frequencies_seen)} frequencies based on {len(deltas)} deltas")
            found_seen_twice = True
            break
        frequencies_seen.add(cur_frequency)



