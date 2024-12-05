# --------------------------------------------------------------------------- #
#    Day 5                                                                    #
# --------------------------------------------------------------------------- #
from functools import cmp_to_key, partial
from pprint import pprint


DAY = 5
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
    orderings, updates = [],[]
    for line in file:
        if "|" not in line:
            orderings = set(orderings)
            break
        orderings.append(tuple(map(int, line.split("|"))))
    for line in file:
        updates.append(tuple(map(int, line.split(","))))
    updates = tuple(updates)

if EXAMPLE:
    pprint(orderings)
    pprint(updates)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #


def is_correct(update):
    for i, n in enumerate(update[:-1]):
        for m in update[i+1:]:
            if (n, m) not in orderings:
                return False
    return True


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(orderings, updates):
    return sum(
        update[len(update) // 2] for update in updates if is_correct(update)
    )


print(solution := part_1(orderings, updates))
assert solution == (143 if EXAMPLE else 6949)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def cmp(a, b):
    return 1 if (a, b) in orderings else -1


key = cmp_to_key(cmp)


def part_2(orderings, updates):
    return sum(
        sorted(update, key=key)[len(update) // 2]
        for update in updates
        if not is_correct(update)
    )


print(solution := part_2(orderings, updates))
assert solution == (123 if EXAMPLE else 4145)
