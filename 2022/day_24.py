# --------------------------------------------------------------------------- #
#    Day 24                                                                   #
# --------------------------------------------------------------------------- #

from collections import Counter
from itertools import cycle
from math import gcd

DAY = 24
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_board(file_name):
    moves = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    with open(file_name, "r") as file:
        next(file)
        rows = [line.rstrip()[1:-1] for line in file]
    rows = rows[:-1]
    blizzards = []
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char != ".":
                blizzards.append(((y, x), moves[char]))
    return len(rows), len(rows[0]), blizzards

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def print_board(height, width, blizzards, E, show=True):
    # Blank board
    strings = [["#", "."] + ["#"] * width] + [
        ["#"] + ["."] * width + ["#"] for _ in range(height)
    ] + [["#"] * width + [".", "#"]]
    
    # Place blizzards on board
    moves = {(-1, 0): "^", (1, 0): "v", (0, -1): "<", (0, 1): ">"}
    multiples = Counter(pos for pos, move in blizzards)
    for (y, x), move in blizzards:
        if (n := multiples.get((y, x), 1)) > 1:
            strings[y + 1][x + 1] = str(n)
        else:
            strings[y + 1][x + 1] = moves[move]
    
    # Place E on board
    Ey, Ex = E
    strings[Ey + 1][Ex + 1] = "E"
    
    string = "\n".join(map("".join, strings))
    if show:
        print("\n" + string + "\n")
    return string


def get_holes(height, width, blizzards):
    period = (height * width) // gcd(height, width)
    grid = {(y, x) for y in range(height) for x in range(width)}
    holes = []
    for _ in range(period):
        blizzards = [
            (((y + dy) % height, (x + dx) % width), (dy, dx))
            for (y, x), (dy, dx) in blizzards
        ]
        holes.append(grid.difference(position for position, _ in blizzards))
    return cycle(holes)


def moves(holes, E):
    # E moves if possible
    Ey, Ex = E
    for dy, dx in (-1, 0), (0, -1), (1, 0), (0, 1):
        y, x = Ey + dy, Ex + dx
        if (y, x) in holes:
            yield y, x
    
    # E stays put if possible
    if E in holes:
        yield E

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def search_path(next_holes, start, stop):
    minute, positions = 0, {start}
    while True and len(positions) > 0:
        minute += 1
        holes = next(next_holes) | {start, stop}
        new_positions = (moves(holes, position) for position in positions)
        positions = set().union(*new_positions)
        if stop in positions:
            break
    return minute


height, width, blizzards = get_board(file_name)
next_holes = get_holes(height, width, blizzards)
minutes = search_path(next_holes, (-1, 0), (height, width - 1))
print(minutes)  # 240

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

minutes += search_path(next_holes, (height, width - 1), (0, 0))
minutes += search_path(next_holes, (-1, 0), (height, width - 1))
print(minutes)  # 717
