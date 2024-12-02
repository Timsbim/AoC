# --------------------------------------------------------------------------- #
#    Day 4                                                                    #
# --------------------------------------------------------------------------- #
import re
from collections import Counter
from pprint import pprint


DAY = 4
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2016/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

names = []
pattern = re.compile(r"([a-z-]+)-(\d+)\[([a-z]+)\]$")
with open(file_name, "r") as file:
    for row in file:
        m = pattern.match(row.strip())
        names.append((tuple(m[1].split("-")), int(m[2]), m[3]))
names = tuple(names)
if EXAMPLE:
    pprint(names)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def is_real(letters, checksum):
    counts = Counter(sorted("".join(letters)))
    return "".join(c for c, _ in counts.most_common(5)) == checksum


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(names):
    return sum(
        ID
        for letters, ID, checksum in names
        if is_real(letters, checksum)
    )


print(solution := part_1(names))
assert solution == (1514 if EXAMPLE else 278221)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def decrypt(letters, cipher):
    shift = cipher - 97
    words = []
    for word in letters:
        words.append("".join(chr(97 + (ord(c) + shift) % 26) for c in word))
    return " ".join(words)


def part_2(names):
    for letters, ID, checksum in names:
        if is_real(letters, checksum):
            decrypted = decrypt(letters, ID)
            if "northpole" in decrypted:
                return ID


print(solution := part_2(names))
assert solution == (None if EXAMPLE else 267)
