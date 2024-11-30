# --------------------------------------------------------------------------- #
#    Day 13                                                                   #
# --------------------------------------------------------------------------- #
from itertools import product
from pprint import pprint


DAY = 13
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
    patterns = [[]]
    for line in file:
        line = line.strip()
        if line == "":
            patterns.append([])
        else:
            patterns[-1].append(line)
if EXAMPLE:
    pprint(patterns)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def col_identity(pattern, c1, c2):
    height = len(pattern)
    return all(pattern[r][c1] == pattern[r][c2] for r in range(height))


def find_reflection(pattern, r0, c0):
    height, width = len(pattern), len(pattern[0])

    last_row = pattern[0]
    for r, row in enumerate(pattern[1:], 1):
        if row == last_row:
            if r != r0 and (r == 1 or all(
                row0 == row1
                for row0, row1 in zip(pattern[r-2::-1], pattern[r+1:])
            )):
                return r, 0
        last_row = row        

    last_c = 0
    for c in range(1, width):
        if col_identity(pattern, last_c, c):
            if c != c0 and (c == 1 or all(
                col_identity(pattern, c1, c2)
                for c1, c2 in zip(range(c-2, -1, -1), range(c+1, width))
            )):
                return 0, c
        last_c = c

    return 0, 0


def part_1(patterns):
    res = 0
    for pattern in patterns:
        r, c = find_reflection(pattern, 0, 0)
        res += r * 100 + c
    return res


solution = part_1(patterns)
assert solution == (405 if EXAMPLE else 42974)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def repair_pattern(pattern):
    height, width = len(pattern), len(pattern[0])
    pattern = [*map(list, pattern)]
    for r, c in product(range(height), range(width)):
        char = pattern[r][c]
        pattern[r][c] = "." if char == "#" else "#"
        yield pattern
        pattern[r][c] = char
    

def part_2(patterns):
    res = 0
    for p, pattern in enumerate(patterns, 1):
        r0, c0 = find_reflection(pattern, 0, 0)
        reflection = False
        for repaired in repair_pattern(pattern):
            r, c = find_reflection(repaired, r0, c0)
            if 0 < (score := r * 100 + c):
                res += score
                reflection = True
                break
    return res


solution = part_2(patterns)
assert solution == (400 if EXAMPLE else 27587)
print(solution)
