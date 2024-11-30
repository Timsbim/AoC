# --------------------------------------------------------------------------- #
#    Day 3                                                                   #
# --------------------------------------------------------------------------- #

DAY = 3
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2022/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    rucksacks = [line.strip() for line in file]
#print(rucksacks)

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

from string import ascii_letters as letters

PRIORITIES = dict((l, p) for p, l in enumerate(letters, start=1))
print(PRIORITIES)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

result = 0
for sack in rucksacks:
    size = len(sack) // 2
    common = (set(sack[:size]) & set(sack[size:])).pop()
    result += PRIORITIES[common]
print(result)


# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

from itertools import groupby

result = 0
for _, group in groupby(enumerate(rucksacks), key=lambda t: t[0] // 3):
    common = set.intersection(*(set(sack) for _, sack in group)).pop()
    result += PRIORITIES[common]
print(result)
