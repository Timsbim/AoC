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

file_name = f"2015/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    instructions = []
    for line in file:
        line = line.replace("turn ", "").replace(" through ", ",")
        cmd, limits = line.split()
        instructions.append((cmd, *map(int, limits.split(","))))
if EXAMPLE:
    pprint(instructions)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

lights = [[0 for _ in range(1_000)] for _ in range(1_000)]

def part_1():
    for cmd, x1, y1, x2, y2 in instructions:
        coverd = product(range(x1, x2 + 1), range(y1, y2 + 1))
        if cmd == "on":
            for x, y in coverd:
                lights[x][y] = 1
        elif cmd == "off":
            for x, y in coverd:
                lights[x][y] = 0
        else:
            for x, y in coverd:
                if lights[x][y] == 0:
                    lights[x][y] = 1
                else:
                    lights[x][y] = 0
    return sum(sum(row) for row in lights)


solution = part_1()
if not EXAMPLE:
    assert solution == 377891
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

lights = [[0 for _ in range(1_000)] for _ in range(1_000)]


def part_2():
    for cmd, x1, y1, x2, y2 in instructions:
        coverd = product(range(x1, x2 + 1), range(y1, y2 + 1))
        if cmd == "on":
            for x, y in coverd:
                lights[x][y] += 1
        elif cmd == "off":
            for x, y in coverd:
                if lights[x][y] > 0:
                    lights[x][y] -= 1
        else:
            for x, y in coverd:
                lights[x][y] += 2
    return sum(sum(row) for row in lights)


solution = part_2()
if not EXAMPLE:
    assert solution == 14110788
print(solution)
