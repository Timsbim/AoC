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

"""
4. floor: nothing
3. floor: PG, PM, RG, RM
2. floor: PM, SM
1. floor: TG, TM, PG, SG

4. floor: nothing
3. floor: PG, PM, RG, RM
2. floor: PG, PM, SG, SM
1. floor: TG, TM

4. floor: nothing
3. floor: PG, PM, RG, RM, SG, SM
2. floor: PG, PM
1. floor: TG, TM

4. floor: SG, SM
3. floor: PG, PM, RG, RM
2. floor: PG, PM
1. floor: TG, TM

4. floor: SM
3. floor: PG, PM, RG, RM, SG
2. floor: PG, PM
1. floor: TG, TM

4. floor: SM
3. floor: PG, PM, RG, RM
2. floor: PG, PM, SG
1. floor: TG, TM

4. floor: SM
3. floor: PG, PM, RG, RM
2. floor: PG, PM
1. floor: TG, TM, SG

4. floor: SM
3. floor: PG, PM, RG, RM
2. floor: PG, PM, TG, SG
1. floor: TM

4. floor: SM
3. floor: PG, PM, RG, RM, TG, SG
2. floor: PG, PM
1. floor: TM

4. floor: SG, SM, TG
3. floor: PG, PM, RG, RM, PG 
2. floor: PM
1. floor: TM

4. floor: SG, SM
3. floor: PG, PM, RG, RM, PG, TG 
2. floor: PM
1. floor: TM

4. floor: SG, SM, PG, TG
3. floor: PG, PM, RG, RM
2. floor: PM
1. floor: TM

4. floor: SG, SM, TG
3. floor: PG, PM, RG, RM, PG
2. floor: PM
1. floor: TM

4. floor: SG, SM, TG
3. floor: PG, PM, RG, RM
2. floor: PG, PM
1. floor: TM

4. floor: SG, SM, TG
3. floor: PG, PM, RG, RM, PG, PM
2. floor: 
1. floor: TM

4. floor: SG, SM, PG, PM, TG
3. floor: PG, PM, RG, RM
2. floor: 
1. floor: TM

4. floor: SG, SM, PG, PM
3. floor: PG, PM, RG, RM, TG
2. floor: 
1. floor: TM

4. floor: SG, SM, PG, PM
3. floor: PG, PM, RG, TG
2. floor: RM
1. floor: TM

4. floor: SG, SM, PG, PM
3. floor: PG, PM, RG, TG
2. floor: 
1. floor: TM, RM

4. floor: SG, SM, PG, PM
3. floor: PG, PM, RG, TG
2. floor: TM, RM
1. floor: 

4. floor: SG, SM, PG, PM
3. floor: PG, PM, RG, TG
2. floor: TM, RM
1. floor: 

"""

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

from bisect import insort_left


# ('TG', 'TM', 'PG', 'SG')

items = ['PG', 'SG', 'TG', 'TM']
insort_left(items, 'SM')
pprint(items)

