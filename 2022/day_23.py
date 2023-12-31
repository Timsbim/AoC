# --------------------------------------------------------------------------- #
#    Day 23                                                                   #
# --------------------------------------------------------------------------- #

from collections import Counter
from itertools import cycle, islice

DAY = 23
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

def get_elves(file_name):
    with open(file_name, "r") as file:
        rows = file.read().splitlines()
    return {
        (j, i)
        for j, row in enumerate(rows) for i, char in enumerate(row)
        if char == "#"
    }

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

RULES = "N", "S", "W", "E"


def get_grid(elves):
    left = up = float("inf")
    right = down = float("-inf")
    for y, x in elves:
        if x < left:
            left = x
        if y < up:
            up = y
        if right < x:
            right = x
        if down < y:
            down = y
    return left, right, up, down


def print_elves(elves):
    left, right, up, down = get_grid(elves)
    width, height = right - left + 1, down - up + 1
    rectangle = [["."] * width for _ in range(height)]
    for y, x in elves:
        rectangle[y - left][x - up] = "#"
    print(
        "+" + width * "-" + "+\n"
        + "\n".join("|" + "".join(row) + "|" for row in rectangle)
        + "\n+" + width * "-" + "+"
    )


def to_check(elve, rule):
    y, x = elve
    if rule == "N":
        y -= 1
        return {(y, x - 1), (y, x), (y, x + 1)}
    if rule == "S":
        y += 1
        return {(y, x - 1), (y, x), (y, x + 1)}
    if rule == "E":
        x += 1
        return {(y - 1, x), (y, x), (y + 1, x)}
    if rule == "W":
        x += -1
        return {(y - 1, x), (y, x), (y + 1, x)}


def move_elve(elve, rule):
    y, x = elve
    if rule == "N":
        return y - 1, x
    if rule == "S":
        return y + 1, x
    if rule == "E":
        return y, x + 1
    if rule == "W":
        return y, x - 1


def check_rules(elves, rules):
    stays, proposals = set(), {}
    for elve in elves:
        first_empty, all_empty = None, True
        for rule in rules:
            if to_check(elve, rule).isdisjoint(elves):
                if first_empty is None:
                    first_empty = rule    
            elif all_empty:
                all_empty = False
        if not all_empty and first_empty is not None:
            proposals[elve] = move_elve(elve, first_empty)
        else:
            stays.add(elve)
    uniques = {
        end
        for end, count in Counter(proposals.values()).items()
        if count == 1
    }
    take = uniques - stays
    return {start: end for start, end in proposals.items() if end in take}


def move_elves(elves, moves):
    elves.difference_update(moves.keys())
    elves.update(moves.values())

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def num_empty_tiles(elves):
    left, right, up, down = get_grid(elves)
    return (right - left + 1) * (down - up + 1) - len(elves)
    
 
elves = get_elves(file_name)
rules = cycle(RULES)
for _ in range(10):
    moves = check_rules(elves, list(islice(rules, 4)))
    move_elves(elves, moves)
    next(rules)
print(num_empty_tiles(elves))  # 4181

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

elves = get_elves(file_name)
rules = cycle(RULES)
n = 0
while True:
    n += 1
    moves = check_rules(elves, list(islice(rules, 4)))
    if len(moves) == 0:
        break
    move_elves(elves, moves)
    next(rules)
print(n)  # 973
