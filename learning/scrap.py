import re

with open('scrap.txt', 'r') as f:
    lines = f.readlines()

odf_lines = [line.strip() for line in lines]

for odf_line in odf_lines:
    number = odf_line.split()[2]
    result = re.match(r"[^0-9]", number)
    if result != None:
        print(f"{odf_line}")
