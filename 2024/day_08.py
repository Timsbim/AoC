# --------------------------------------------------------------------------- #
#    Day 8                                                                    #
# --------------------------------------------------------------------------- #
from itertools import combinations
from pprint import pprint


DAY = 8
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

antennas = {}
with open(file_name, "r") as file:
    lines = [line.rstrip() for line in file]
ROWS, COLS = len(lines), len(lines[0])
for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if char != ".":
            antennas.setdefault(char, []).append((r, c))
if EXAMPLE:
    pprint(antennas)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(antennas):
    antinodes = set()
    for positions in antennas.values():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            for r, c in (2 * r1 - r2, 2 * c1 - c2), (2 * r2 - r1, 2 * c2 - c1):
                if 0 <= r < ROWS and 0 <= c < COLS:
                    antinodes.add((r, c))
    return len(antinodes)


print(solution := part_1(antennas))
assert solution == (14 if EXAMPLE else 327)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(antennas):
    antinodes = set()
    for positions in antennas.values():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            for r, c, dr, dc in (r1, c1, r1 - r2, c1 - c2), (r2, c2, r2 - r1, c2 - c1):
                while 0 <= r < ROWS and 0 <= c < COLS:
                    antinodes.add((r, c))
                    r, c = r + dr, c + dc
    return len(antinodes)


print(solution := part_2(antennas))
assert solution == (34 if EXAMPLE else 1233)
