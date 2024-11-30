# --------------------------------------------------------------------------- #
#    Day 16                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 16
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
    layout = file.read().splitlines()
if EXAMPLE:
    pprint(layout)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def next_step(tile, y, x, direction):
    if tile == ".":
        if direction == ">":
            yield y, x + 1, ">"
        elif direction == "v":
            yield y + 1, x, "v"
        elif direction == "<":
            yield y, x - 1, "<"
        else:
            yield y - 1, x, "^" 
    
    elif tile == "/":
        if direction == ">":
            yield y - 1, x, "^"
        elif direction == "v":
            yield y, x - 1, "<"
        elif direction == "<":
            yield y + 1, x, "v"
        else:
            yield y, x + 1, ">"
    
    elif tile == "\\":
        if direction == ">":
            yield y + 1, x, "v"
        elif direction == "v":
            yield y, x + 1, ">"
        elif direction == "<":
            yield y - 1, x, "^"
        else:
            yield y, x - 1, "<"
    
    elif tile == "|":
        if direction == ">" or direction == "<":
            yield y + 1, x, "v"
            yield y - 1, x, "^"
        elif direction == "v":
            yield y + 1, x, "v"
        else:
            yield y - 1, x, "^"
    
    else:
        if direction == "^" or direction == "v":
            yield y, x - 1, "<"
            yield y, x + 1, ">"
        elif direction == ">":
            yield y, x + 1, ">"
        else:
            yield y, x - 1, "<"


def stepping(layout, start):
    height, width = len(layout), len(layout[0])
    energized, steps, visited = set(), [start], {start}
    while steps:
        next_steps = []
        for y, x, direction in steps:
            if 0 <= y < height and 0 <= x < width:
                energized.add((y, x))
                for step in next_step(layout[y][x], y, x, direction):
                    if step not in visited:
                        next_steps.append(step)
                        visited.add(step)
        steps = next_steps
    return len(energized)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(layout):
    return stepping(layout, (0, 0, ">"))


solution = part_1(layout)
assert solution == (46 if EXAMPLE else 7242)
pprint(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def starts(height, width):
    max_y, max_x = height - 1, width - 1
    for x in range(width):
        yield 0, x, "v"
        yield max_y, x, "^"
    for y in range(height):
        yield y, 0, ">"
        yield y, max_x, "<"


def part_2(layout):
    height, width = len(layout), len(layout[0]) 
    max_energy = 0
    for start in starts(height, width):
        max_energy = max(stepping(layout, start), max_energy)
    return max_energy


solution = part_2(layout)
assert solution == (51 if EXAMPLE else 7572)
print(solution)
