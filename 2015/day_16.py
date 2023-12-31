# --------------------------------------------------------------------------- #
#    Day 16                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 16

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/day_{DAY:0>2}_input.txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

AUNT_SUE = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


with open(file_name, "r") as file:
    sues = []
    for line in file:
        sues.append({})
        compounds = line.split(": ", 1)[1]
        for compound in compounds.split(", "):
            compound, num = compound.split(": ")
            sues[-1][compound] = int(num)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(sues):
    for n, sue in enumerate(sues, start=1):
        if all(
            AUNT_SUE[compound] == quantity
            for compound, quantity in sue.items() if quantity != 0
        ):
            return n


solution = part_1(sues)
assert solution == 40
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def check(compound, quantity):
    aunt_sue_quantity = AUNT_SUE[compound]
    if aunt_sue_quantity == 0:
        return False
    if compound in ("cats", "trees"):
        return quantity > aunt_sue_quantity
    if compound in ("pomeranians", "goldfish"):
        return quantity < aunt_sue_quantity
    return aunt_sue_quantity == quantity


def part_2(sues):
    for n, sue in enumerate(sues, start=1):
        if all(
            check(compound, quantity)
            for compound, quantity in sue.items()
        ):
            return n


solution = part_2(sues)
assert solution == 241
print(solution)
