# --------------------------------------------------------------------------- #
#    Day 11                                                                   #
# --------------------------------------------------------------------------- #
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
 
key = itemgetter(1)
INITIAL_STATE = [
    tuple(tuple(sorted(group)) for _, group in groupby(sorted(floor, key=key), key=key))
    for floor in FLOORS
]
pprint(INITIAL_STATE)
 
generators = sorted(
    part[0]
    for floor in FLOORS
    for part in floor
    if part[1] == "G"
)
TARGET = (
    3,  # Elevator on 4. floor
    (tuple(), tuple()), (tuple(), tuple()), (tuple(), tuple()),  # The first 3 floors are empty
    (tuple(f"{g}G" for g in generators),
     tuple(f"{g}M" for g in generators))  # All parts in 3. floor
)
 

def to_state(floors):
    pass
 

def from_state(state):
    pass
 

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
