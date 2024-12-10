# --------------------------------------------------------------------------- #
#    Day 10                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 10
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
    topos = tuple(tuple(map(int, line.rstrip())) for line in file)
if EXAMPLE:
    pprint(topos)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #
ROWS, COLS = len(topos), len(topos[0])


def moves(r, c):
    for dr, dc in (0, 1), (1, 0), (0, -1), (-1, 0):
        r1, c1 = r + dr, c + dc
        if 0 <= r1 < ROWS and 0 <= c1 < COLS:
            yield r1, c1


def hike(topos):
    score = count = 0
    for r0, row in enumerate(topos):
        for c0, n in enumerate(row):
            if n: continue
            heads = [(r0, c0)]
            for n in range(1, 10):
                heads_new = []
                for r, c in heads:
                    for r1, c1 in moves(r, c):
                        if topos[r1][c1] == n:
                            heads_new.append((r1, c1))
                heads = heads_new
            score += len(set(heads))
            count += len(heads)
    return score, count


solution_1, solution_2 = hike(topos)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #

print(f"Part 1: {solution_1}")
assert solution_1 == (36 if EXAMPLE else 776)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #

print(f"Part 2: {solution_2}")
assert solution_2 == (81 if EXAMPLE else 1657)
