# --------------------------------------------------------------------------- #
#    Day 11                                                                   #
# --------------------------------------------------------------------------- #
from itertools import combinations


DAY = 11
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
    grid = file.read().splitlines()

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

def offsetting(limit, members, base_offset):
    new_members, offset = {}, 0
    for n in range(limit):
        if n in members:
            new_members[n] = n + offset
        else:
            offset += base_offset
    return new_members


def expand(grid, multiple):
    height, width = len(grid), len(grid[0])
    galaxies, rows, cols = [], set(), set()
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "#":
                galaxies.append((y, x))
                rows.add(y)
                cols.add(x)
    new_rows = offsetting(height, rows, multiple - 1)
    new_cols = offsetting(width, cols, multiple - 1)
    new_galaxies = [(new_rows[y], new_cols[x]) for y, x in galaxies]
    return sum(
        abs(y1 - y0) + abs(x1 - x0)
        for (y0, x0), (y1, x1) in combinations(new_galaxies, r=2)
    )

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

solution = expand(grid, 2)
assert solution == (374 if EXAMPLE else 9623138)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

solution = expand(grid, 1_000_000)
assert solution == (82000210 if EXAMPLE else 726820169514)
print(solution)
