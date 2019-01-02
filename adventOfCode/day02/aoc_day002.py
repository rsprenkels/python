with open('box_id_list.txt', 'r') as f:
    box_id_lines = f.read().splitlines()

codes_with_2, codes_with_3 = 0,0

for index, box_id in enumerate(box_id_lines, start=1):
    print(f"checking out id {index}: {box_id}")

    count_dict = {}

    for char in box_id:
        print(f"it has char {char}")
        if char in count_dict:
            count_dict[char] = count_dict[char] + 1
        else:
            count_dict[char] = 1

    print(f"I have seen {count_dict}")

    appears_2 = len([count for count in count_dict.values() if count == 2])
    appears_3 = len([count for count in count_dict.values() if count == 3])

    if appears_2 > 0:
        codes_with_2 += 1
    if appears_3 > 0:
        codes_with_3 += 1

    print(f"I see {appears_2} letters twice and {appears_3} letters three times",
          f"current {codes_with_2} for 2 and {codes_with_3} for 3"
    )

print(f"overall checksum is therefore {codes_with_2 * codes_with_3}")

sorted_ids = sorted(box_id_lines)
found_first = ''
found_second = ''

for index in range(len(sorted_ids) - 1):
    first, second = list(sorted_ids[index:index+2])
    print(f"index {index}\nF {first}\nS {second}", end='')

    chars_differ = 0
    for char_index in range(len(first)):
        if first[char_index] != second[char_index]:
            chars_differ += 1

    print(f" {chars_differ} differ")

    if chars_differ == 1:
        found_first = first
        found_second = second

print(f"foundFirst  {found_first}")
print(f"foundSecond {found_second}")

def get_common(first, second):
    result = ''
    for char_index in range(len(first)):
        if first[char_index] == second[char_index]:
            result += first[char_index]
    return result

print(f"the common part is {get_common(found_first, found_second)}")


