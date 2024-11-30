# --------------------------------------------------------------------------- #
#    Day 12                                                                   #
# --------------------------------------------------------------------------- #
import json
import re


DAY = 12
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    with open(file_name, "r") as file:
        return sum(int(m[0]) for m in re.finditer(r"-?\d+", file.read()))


solution = part_1()
if not EXAMPLE:
    assert solution == 156366
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def sum_numbers(document):
    if isinstance(document, str):
        return 0
    if isinstance(document, int):
        return document
    if isinstance(document, list):
        return sum(map(sum_numbers, document))
    if isinstance(document, dict):
        values = document.values()
        return 0 if "red" in values else sum(map(sum_numbers, values))


def part_2():
    with open(file_name, "r") as file:
        return sum_numbers(json.load(file))


solution = part_2()
if not EXAMPLE:
    assert solution == 96852
print(solution)
