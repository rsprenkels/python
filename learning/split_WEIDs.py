with open('WEIDs.txt', 'r') as f:
    WEIDs = f.readlines()

WEIDs = [weid.strip() for weid in WEIDs]

for weid in WEIDs:
    tzip, nr, *rest = weid.split()
    ext = rest[0] if len(rest) == 2 else ''
    unit = rest[-1]
    print(f"{tzip:8}, {nr:4}, {ext:3}, {unit}")