from sys import version

advent_coin = 'bgvyzdsv'
# advent_coin = 'abcdef'

import hashlib

number = -1
found = False
while not found:
    number += 1
    found = hashlib.md5(f"{advent_coin}{number}".encode()).hexdigest()[0:5] == "00000"

print(f"answer part 1: {number}")

number = -1
found = False
while not found:
    number += 1
    found = hashlib.md5(f"{advent_coin}{number}".encode()).hexdigest()[0:6] == "000000"

print(f"answer part 2: {number}")

