# --------------------------------------------------------------------------- #
#    Day 12                                                                   #
# --------------------------------------------------------------------------- #
from functools import cache
from pprint import pprint


DAY = 12
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    rows = []
    for line in file:
        springs, condition = line.rstrip().split()
        rows.append((springs, tuple(map(int, condition.split(",")))))
if EXAMPLE:
    pprint(rows)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

@cache
def all_free(springs, condition):
    len_condition = len(condition)
    if len_condition == 0:
        return 1
    size = (
        len(springs) + 1
        - sum(condition[1:])
        - (len_condition - 1)
        - condition[0]
    )
    len_condition += 1
    numbers = [1] * len_condition
    for _ in range(size - 1):
        for i in range(1, len_condition):
            numbers[i] += numbers[i-1]
    return numbers[-1]


@cache
def arrange(springs, condition):
    if springs == "" and condition:
        return 0
    if len(condition) == 0:
        return 1 if all(s == "." or s == "?" for s in springs) else 0
    springs = springs.lstrip(".")
    n = condition[0]
    end = springs.find(".")
    if end < 0:
        block, tail = springs, ""
    else:
        block, tail = springs[:end], springs[end:]
    length = len(block)
    if length < n:
        return 0 if "#" in block else arrange(tail, condition)
    count = 0
    if "#" in block:
        stop = min(length - n, block.find("#"))  # <- min(length, block.find("#") + n?
        for i in range(stop + 1):  # <- simplify indexing (move the end of the #-block)
            if (i + n == length) or (block[i+n] != "#"):
                count += arrange(f"{block[i+n+1:]}{tail}", condition[1:])
    else:
        for i in range(len(condition) + 1):
            sub_condition = condition[:i]
            if sum(sub_condition) + i > length + 1:  # <- summing in loop?
                break
            num_block_combos = all_free(block, sub_condition)
            count += num_block_combos * arrange(tail, condition[i:])
    return count

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(rows):
    return sum(arrange(springs, condition) for springs, condition in rows)


solution = part_1(rows)
assert solution == (21 if EXAMPLE else 7169)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(rows):
    count = 0
    for springs, condition in rows:
        springs, condition = "?".join([springs] * 5), condition * 5
        count += arrange(springs, condition)
    return count


solution = part_2(rows)
assert solution == (525152 if EXAMPLE else 1738259948652)
print(solution)
