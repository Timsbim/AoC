# --------------------------------------------------------------------------- #
#    Day 1                                                                    #
# --------------------------------------------------------------------------- #
from collections import Counter
from pprint import pprint


DAY = 1
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2024/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    numbers = tuple(zip(*(map(int, line.split()) for line in file)))

if EXAMPLE:
    pprint(numbers)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(numbers):
    return sum(
        abs(n - m) for n, m in zip(sorted(numbers[0]), sorted(numbers[1]))
    )


print(solution := part_1(numbers))
assert solution == (11 if EXAMPLE else 1320851)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(numbers):
    counts2 = Counter(numbers[1])
    return sum(n * counts2.get(n, 0) for n in numbers[0])


print(solution := part_2(numbers))
assert solution == (31 if EXAMPLE else 26859182)
