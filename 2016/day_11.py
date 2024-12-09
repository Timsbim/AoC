# --------------------------------------------------------------------------- #
#    Day 11                                                                   #
# --------------------------------------------------------------------------- #
from collections import Counter
from itertools import groupby
from pprint import pprint
from operator import itemgetter


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
pprint(FLOORS)


data = sorted(
    (item[1], item[0], n)
    for n, floor in enumerate(FLOORS)
    for item in floor
)
kinds = {i: item[1] for i, item in zip(range(len(data) // 2), data)}
pprint(kinds)
LEN = len(data) // 2
state = 0, tuple(n for _, _, n in data[:LEN]), tuple(n for _, _, n in data[LEN:])
pprint(state)


def to_state(floors):
    pass
 

def from_state(state):
    elevator, gens, chips = state
    floors = [[], [],[], []]
 

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
- If at least 1 generator: if chip => also corresponding generator
- All chips
- All generators
[- Complete chip-generator pairs only <= part of 2. item]
- Non-pairs => generators
 
Possible loads:
 
- 1 or 2 chips
- 1 or 2 generators if: (generator isn't paired) or (no un-paired chip is left)
- pair
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
