# --------------------------------------------------------------------------- #
#    Day 6                                                                    #
# --------------------------------------------------------------------------- #
from itertools import product
from pprint import pprint


DAY = 6
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
    grid = tuple(line.rstrip() for line in file)
ROWS, COLS = len(grid), len(grid[0])
obstacles = set()
for r, line in enumerate(grid):
    for c, char in enumerate(line):
        if char == ".":
            continue
        if char == "#":
            obstacles.add((r, c))
        else:
            start, direction = (r, c), char
if EXAMPLE:
    print(f"{direction = }, {start = }")
    print("obstacles =", obstacles)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(obstacles, direction, start):
    visited, (r, c) = {start}, start
    while True:
        if direction == "^":
            if r == 0:
                return len(visited)
            if (r - 1, c) in obstacles:
                direction = ">"
            else:
                r -= 1
        elif direction == ">":
            if c == COLS - 1:
                return len(visited)
            if (r, c + 1) in obstacles:
                direction = "v"
            else:
                c += 1
        elif direction == "v":
            if r == ROWS - 1:
                return len(visited)
            if (r + 1, c) in obstacles:
                direction = "<"
            else:
                r += 1
        elif direction == "<":
            if c == 0:
                return len(visited)
            if (r, c - 1) in obstacles:
                direction = "^"
            else:
                c -= 1
        visited.add((r, c))


print(solution := part_1(obstacles, direction, start))
assert solution == (41 if EXAMPLE else 4515)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(obstacles, direction, start):
    count, direction_start = 0, direction
    for position in product(range(ROWS), range(COLS)):
        if position in obstacles or position == start:
            continue
        obstacles_mod = obstacles | {position}
        (r, c), direction = start, direction_start
        visited = {(r, c, direction)}
        while True:
            if direction == "^":
                if r == 0:
                    break
                if (r - 1, c) in obstacles_mod:
                    direction = ">"
                else:
                    r -= 1
            elif direction == ">":
                if c == COLS - 1:
                    break
                if (r, c + 1) in obstacles_mod:
                    direction = "v"
                else:
                    c += 1
            elif direction == "v":
                if r == ROWS - 1:
                    break
                if (r + 1, c) in obstacles_mod:
                    direction = "<"
                else:
                    r += 1
            elif direction == "<":
                if c == 0:
                    break
                if (r, c - 1) in obstacles_mod:
                    direction = "^"
                else:
                    c -= 1
            if (r, c, direction) in visited:
                count += 1
                break
            visited.add((r, c, direction))
        
    return count
    

print(solution := part_2(obstacles, direction, start))
assert solution == (6 if EXAMPLE else 1309)
