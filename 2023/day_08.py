# --------------------------------------------------------------------------- #
#    Day 8                                                                    #
# --------------------------------------------------------------------------- #
from itertools import cycle
from math import lcm
from pprint import pprint


DAY = 8
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    lrs = next(file).strip()
    next(file)
    nodes = {}
    for line in file:
        node, lr = line.rstrip().split(" = ")
        left, right = lr.strip("()").split(", ")
        nodes[node] = (left, right)
if EXAMPLE:
    print(lrs)
    pprint(nodes)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    moves = cycle(lrs)
    start, num = "AAA", 0
    while True:
        num += 1
        left, right = nodes[start]
        start = left if next(moves) == "L" else right
        if start == "ZZZ":
            break
    return num


solution = part_1()
assert solution == 17873
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    moves = cycle(lrs)
    stops = []
    for start in (node for node in nodes if node.endswith("A")):
        num = 0
        while True:
            num += 1
            left, right = nodes[start]
            start = left if next(moves) == "L" else right
            if start.endswith("Z"):
                stops.append(num)
                break
    return lcm(*stops)


solution = part_2()
assert solution == 15746133679061
print(solution)
