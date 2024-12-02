# --------------------------------------------------------------------------- #
#    Day 11                                                                   #
# --------------------------------------------------------------------------- #
from itertools import groupby
from pprint import pprint


DAY = 11
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

FLOORS = (
    (('HM', 'LM'), ('HG',), ('LG',))
    if EXAMPLE else
    (('TG', 'TM', 'PG', 'SG'), ('PM', 'SM'), ('PG', 'PM', 'RG', 'RM'))
)
print(tuple(tuple(sorted(floor)) for floor in FLOORS))
pprint((tuple(), tuple(), tuple(), tuple(sorted(item for floor in FLOORS for item in floor))))
def key(item): return item[-1]
pprint(tuple(
    tuple(sorted(group))
    for floor in FLOORS
    for k, group in groupby(sorted(floor, key=key), key=key)
))

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def print_floors(floors):
    pass

  
# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

"""
Possible floor constellations:
- Empty
- All chips
- All generators
- Complete chip-generator pairs only
"""


def part_1():
    return None


print(solution := part_1())
#assert solution == (if EXAMPLE else)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return None


print(solution := part_2())
#assert solution == (if EXAMPLE else)
