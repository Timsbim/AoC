# --------------------------------------------------------------------------- #
#    Day 6                                                                    #
# --------------------------------------------------------------------------- #
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
print(ROWS * COLS)
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
    print(f"{start = }, {direction = }")
    print(f"{obstacles = }")

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

DIRECTION = dict(zip("^>v<", range(4)))
DELTA = (-1, 0), (0, 1), (1, 0), (0, -1)


def visit(obstacles, start, direction):
    visited, (r, c), direction = {start}, start, DIRECTION[direction]
    while True:
        dr, dc = DELTA[direction]
        r1, c1 = r + dr, c + dc
        if r1 < 0 or r1 == ROWS or c1 < 0 or c1 == COLS:
            return visited
        if (r1, c1) in obstacles:
            direction = (direction + 1) % 4
        else:
            r, c = r1, c1
            visited.add((r, c)) 


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(obstacles, start, direction):
    return len(visit(obstacles, start, direction))


print(solution := part_1(obstacles, start, direction))
assert solution == (41 if EXAMPLE else 4515)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(obstacles, start, direction):
    count, direction_start = 0, DIRECTION[direction]
    for position in visit(obstacles, start, direction) - {start}:
        obstacles_mod = obstacles | {position}
        (r, c), direction = start, direction_start
        visited = {(r, c, direction)}
        while True:
            dr, dc = DELTA[direction]
            r1, c1 = r + dr, c + dc
            if r1 < 0 or r1 == ROWS or c1 < 0 or c1 == COLS:
                break
            if (r1, c1) in obstacles_mod:
                direction = (direction + 1) % 4
            else:
                r, c = r1, c1
            if (r, c, direction) in visited:
                count += 1
                break
            visited.add((r, c, direction))        
    return count
    

print(solution := part_2(obstacles, start, direction))
assert solution == (6 if EXAMPLE else 1309)
