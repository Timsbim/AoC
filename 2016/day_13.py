# --------------------------------------------------------------------------- #
#    Day 13                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 13
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

NUMBER = 10 if EXAMPLE else 1364

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def layout(x, y):
    b = bin(x * x + 3 * x + 2 * x * y + y + y * y + NUMBER)[2:]
    return "#" if b.count("1") % 2 else "."


def step(grid, visited, rim):
    rim_new = []
    for x, y in rim:
        for dx, dy in (0, 1), (1, 0), (0, -1), (-1, 0):
            x1, y1 = x + dx, y + dy
            if x1 < 0 or y1 < 0 or (x1, y1) in visited:
                continue
            if (x1, y1) not in grid:
                grid[x1, y1] = layout(x1, y1)
            if grid[x1, y1] == ".":
                rim_new.append((x1, y1))
                visited.add((x1, y1))
    return rim_new


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(target):
    count, grid, visited, rim = 0, {(1, 1): layout(1, 1)}, {(1, 1)}, [(1, 1)]
    while True:
        count += 1
        rim = step(grid, visited, rim)
        if target in visited:
            return count


print(solution := part_1((7, 4) if EXAMPLE else (31, 39)))
assert solution == (11 if EXAMPLE else 86)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    grid, visited, rim = {(1, 1): layout(1, 1)}, {(1, 1)}, [(1, 1)]
    for _ in range(50):
        rim = step(grid, visited, rim)
    return len(visited)


print(solution := part_2())
assert solution == (151 if EXAMPLE else 127)
