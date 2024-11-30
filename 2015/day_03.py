# --------------------------------------------------------------------------- #
#    Day 3                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 3
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    directions = file.read().rstrip()
if EXAMPLE:
    pprint(directions)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def move(position, direction):
    x, y = position
    if direction == ">":
        return x + 1, y
    if direction == "<":
        return x - 1, y
    if direction == "^":
        return x, y + 1
    return x, y - 1

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    position, houses = (0, 0), {(0, 0)}
    for direction in directions:
        position = move(position, direction)
        houses.add(position)
    return len(houses)


solution = part_1()
if not EXAMPLE:
    assert solution == 2592
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    position, houses = (0, 0), {(0, 0)}
    for direction in directions[0::2]:
        position = move(position, direction)
        houses.add(position)
    position = (0, 0)
    for direction in directions[1::2]:
        position = move(position, direction)
        houses.add(position)
    return len(houses)


solution = part_2()
if not EXAMPLE:
    assert solution == 2360
print(solution)
