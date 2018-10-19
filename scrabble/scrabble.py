f = open("wordlist.txt", "r")

words = []

for line in f:
    line = line.strip()
    words.append(line.split("\t")[0])

f.close()

print(f"there are {len(words)} words in the list")

words_with_start = 0
for word in words:
    if word[0] == 'A':
        words_with_start += 1

print(f"there are {words_with_start} words starting with A")


def has_double_vowel(word):
    vowels = "AEOIU"
    for vowel in vowels:
        double_vowel = vowel * 2
        if double_vowel in word:
            return True
    return False

for word in words:
    if has_double_vowel(word):
        print(f"{word} has a double vowel")

def has_all_vowels(word):
    for vowel in "AEOUI":
        if vowel not in word:
            return False
    return True

count_all_vowels = 0

for word in words:
    if has_all_vowels(word):
        count_all_vowels += 1
        print(f"{word} has all vowels")

print(f"{count_all_vowels} words have all vowels")