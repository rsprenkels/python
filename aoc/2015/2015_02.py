gifts = open('2015_02_input.txt', 'r').readlines()

# gifts = ['2x3x4']
total_area = 0
ribbon = 0

for gift in gifts:
    l, w, h = map(int, gift.split('x'))
    total_area += (l * w + l * h + w * h) * 2
    total_area += min(l * w, l * h, w * h)
    ribbon += min(l + w, l + h, w + h) * 2 + l * w * h

print(f"area {total_area} ribbon {ribbon}")

# wrong:    1513618.0
#           1586300.0
