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

antennaes = {}
with open(file_name, "r") as file:
    lines = [line.rstrip() for line in file]
ROWS, COLS = len(lines), len(lines[0])
for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if char != ".":
            antennaes.setdefault(char, []).append((r, c))
if EXAMPLE:
    pprint(antennaes)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(antennaes):
    antinodes = set()
    for antenna, positions in antennaes.items():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            dr, dc = r1 - r2, c1 - c2
            r, c = r1 + dr, c1 + dc
            if 0 <= r and r < ROWS and 0 <= c and c < COLS:
                antinodes.add((r, c))
            r, c = r2 - dr, c2 - dc
            if 0 <= r and r < ROWS and 0 <= c and c < COLS:
                antinodes.add((r, c))
    return len(antinodes)


print(solution := part_1(antennaes))
assert solution == (14 if EXAMPLE else 327)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(antennaes):
    antinodes = set().union(*antennaes.values())
    for antenna, positions in antennaes.items():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            dr, dc = r1 - r2, c1 - c2
            r, c = r1, c1
            while True:
                r, c = r + dr, c + dc
                if 0 <= r and r < ROWS and 0 <= c and c < COLS:
                    antinodes.add((r, c))
                else:
                    break
            r, c = r2, c2
            while True:
                r, c = r - dr, c - dc
                if 0 <= r and r < ROWS and 0 <= c and c < COLS:
                    antinodes.add((r, c))
                else:
                    break
    return len(antinodes)


print(solution := part_2(antennaes))
assert solution == (39 if EXAMPLE else 1233)
