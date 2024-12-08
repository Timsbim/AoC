# --------------------------------------------------------------------------- #
#    Day 20                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 20
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
    intervals = tuple(
        sorted(tuple(map(int, line.split("-"))) for line in file)
    )
if EXAMPLE:
    pprint(intervals)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(intervals):
    right = intervals[0][1]
    for a, b in intervals[1:]:
        if right < a - 1:
            return right + 1
        right = max(right, b)


print(solution := part_1(intervals))
assert solution == (3 if EXAMPLE else 31053880)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(intervals):
    count, right = 0, intervals[0][1]
    for a, b in intervals[1:]:
        if right < a - 1:
            count += a - right - 1
        right = max(right, b)
    return count


print(solution := part_2(intervals))
assert solution == (1 if EXAMPLE else 117)
