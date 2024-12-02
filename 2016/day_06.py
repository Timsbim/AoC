# --------------------------------------------------------------------------- #
#    Day 6                                                                    #
# --------------------------------------------------------------------------- #
from collections import Counter
from pprint import pprint


DAY = 6
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
    columns = tuple(zip(*(row.strip() for row in file)))

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(columns):
    return "".join(Counter(column).most_common(1)[0][0] for column in columns)


print(solution := part_1(columns))
assert solution == ("easter" if EXAMPLE else "xdkzukcf")

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(columns):
    return "".join(Counter(column).most_common()[-1][0] for column in columns)


print(solution := part_2(columns))
assert solution == ("advent" if EXAMPLE else "cevsgyvd")
