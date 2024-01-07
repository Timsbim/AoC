# --------------------------------------------------------------------------- #
#    Day 24                                                                   #
# --------------------------------------------------------------------------- #
from itertools import combinations
from math import prod
from pprint import pprint


DAY = 24
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    PACKAGES = tuple(map(int, file))

if EXAMPLE:
    pprint(PACKAGES)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def pack(group_weight):
    qe, found = float("inf"), False
    for r in range(1, len(PACKAGES)):
        if found:
            break
        for packages in combinations(PACKAGES, r):
            if sum(packages) == group_weight:
                found = True
                qe = min(qe, prod(packages))

    return qe

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    return pack(sum(PACKAGES) // 3)


solution = part_1()
assert solution == (99 if EXAMPLE else 11266889531)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return pack(sum(PACKAGES) // 4)


solution = part_2()
assert solution == (44 if EXAMPLE else 77387711)
print(solution)
