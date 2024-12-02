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

file_name = f"2016/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    triplets = tuple(tuple(map(int, row.split())) for row in file)
if EXAMPLE:
    pprint(triplets)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def is_triangle(triple):
    a, b, c = triple
    return a + b > c and a + c > b and b + c > a


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    return sum(map(is_triangle, triplets))


print(solution := part_1())
assert solution == (3 if EXAMPLE else 1050)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return sum(
        is_triangle(column[i:i+3])
        for column in zip(*triplets)
        for i in range(0, len(column), 3)
    )


print(solution := part_2())
assert solution == (6 if EXAMPLE else 1921)
