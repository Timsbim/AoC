# --------------------------------------------------------------------------- #
#    Day 22                                                                   #
# --------------------------------------------------------------------------- #
import re
from itertools import combinations
from pprint import pprint


DAY = 22
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

NODES = {}
with open(file_name, "r") as file:
    next(file); next(file)
    re_data = re.compile(r"x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T")
    for line in file:
        x, y, size, used = map(int, re_data.search(line).groups())
        NODES[y, x] = size, used
if EXAMPLE:
    pprint(NODES)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

ROWS = COLS = 0
for y, x in NODES.keys():
    if y > ROWS:
        ROWS = y
    if x > COLS:
        COLS = x
ROWS += 1
COLS += 1

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    count = 0
    for n1, n2 in combinations(NODES.values(), 2):
        size1, used1 = n1
        size2, used2 = n2
        used = used1 + used2
        if used1 != 0 and used <= size2:
            count += 1
        if used2 != 0 and used <= size1:
            count += 1
    return count


print(solution := part_1())
assert solution == (7 if EXAMPLE else 888)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="\n")

# The only node that can take a load from any other node is the only empty node


def usable_nodes():
    nodes = set()
    for (y1, x1), (y2, x2) in combinations(NODES.keys(), 2):
        size1, used1 = NODES[y1, x1]
        size2, used2 = NODES[y2, x2]
        used = used1 + used2
        if used1 != 0 and used <= size2:
            nodes.add((y2, x2))
        if used2 != 0 and used <= size1:
            nodes.add((y1, x1))
    return nodes


usable = usable_nodes()
assert len(usable) == 1
Y, X = usable.pop()

# => the only moves possible are through moving the empty node


# 1. step: find shortest paths to move empty node adjacent to goal node
def part_21():
    targets = {(0, COLS - 2), (1, COLS - 1)}
    results = []
    steps, paths, visited = 0, [(Y, X)], set()
    while targets and paths:
        steps += 1
        paths_new = []
        for y, x in paths:
            size = NODES[y, x][0]
            for dy, dx in (0, 1), (1, 0), (0, -1), (-1, 0):
                p = y + dy, x + dx
                if p in NODES and p not in visited:
                    if NODES[p][1] > size:
                        continue
                    if p in targets:
                        results.append((steps, p))
                        targets.remove(p)
                    else:
                        paths_new.append(p)
                    visited.add(p)
        paths = paths_new
    return results


print(" and ".join(f"{y}-{x}: {s}" for s, (y, x) in sorted(part_21())))
steps = 1 if EXAMPLE else 60

# 2. step: move goal load to (0, COLS-2) and empty node to (0, COLS-1)
steps += 1

# 3. step: Check if straight-forward solution is possible => yes
min_size = min(NODES[r, c][0] for r in range(2) for c in range(COLS))
max_used = max(NODES[r, c][1] for r in range(2) for c in range(COLS))
assert max_used <= min_size

# => move goal load left on first row: go around with empty node and then move
# => 5 steps per move, ie. 5 * (COLS - 2) steps in total

solution = (1 if EXAMPLE else 60) + 1 + 5 * (COLS - 2)
print(f"{solution = }")
assert solution == (7 if EXAMPLE else 236)
