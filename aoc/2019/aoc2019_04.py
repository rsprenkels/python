def is_valid(combi: int, second_test: callable = lambda digits, x: True) -> bool:
    digits = [int(d) for d in str(combi)]
    for x in range(len(digits) - 1):
        if digits[x + 1] < digits[x]:
            return False
    for x in range(len(digits) - 1):
        if digits[x + 1] == digits[x] and second_test(digits, x):
            return True
    return False


def part_2_test(digits, x) -> bool:
    if x == 0 and digits[2] != digits[0]:
        return True
    if x == len(digits) - 2 and digits[x - 1] != digits[x]:
        return True
    if digits[x - 1] != digits[x] and digits[x + 2] != digits[x]:
        return True
    return False

def is_valid_2(combi) -> bool:
    return is_valid(combi, second_test=part_2_test)

def password_combis(in_from, in_to, valid_func=is_valid):
    valid_count = 0
    for combi in range(in_from, in_to + 1):
        if valid_func(combi):
            valid_count += 1
    return valid_count

def test_p1():
    assert password_combis(145852,616942, is_valid) == 1767

def test_p2():
    assert password_combis(145852,616942, is_valid_2) == 1192

def test_1():
    assert is_valid(111111) == True

def test_2():
    assert is_valid(223450) == False

def test_3():
    assert is_valid(123789) == False

if __name__ == '__main__':
    print(f"aoc 2019 day 03 part 1 {password_combis(145852,616942)}")
    print(f"aoc 2019 day 03 part 1 {password_combis(145852,616942, valid_func=is_valid_2)}")
