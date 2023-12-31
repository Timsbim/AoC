# --------------------------------------------------------------------------- #
#    Day 3                                                                    #
# --------------------------------------------------------------------------- #
import re


DAY = 3
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
    schematic = file.read().splitlines()

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

re_digits = re.compile(r"\d+")

height, width = len(schematic), len(schematic[0])


def border(r, c0, c1):
    if 0 < c0:
        start = c0 - 1
        yield r, start
    else:
        start = 0
    if c1 < width:
        end = c1
        yield r, end
    else:
        end = width - 1
    cs = range(start, end + 1)
    if 0 < r:
        r0 = r - 1
        for c in cs:
            yield r0, c
    if r < height - 1:
        r1 = r + 1
        for c in cs:
            yield r1, c

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    solution = 0
    for r, row in enumerate(schematic):
        for match in re_digits.finditer(row):
            for x, y in border(r, match.start(), match.end()):
                char = schematic[x][y]
                if char != "." and not char.isdigit():
                    solution += int(match[0])
                    break
    return solution


solution = part_1()
assert solution == 540025
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    gear_digits = {
        (r, c): []
        for r, row in enumerate(schematic)
        for c, char in enumerate(row)
        if char == "*"
    }
    gears = set(gear_digits.keys())   
    for r, row in enumerate(schematic):
        for match in re_digits.finditer(row):
            number = int(match[0])
            c0, c1 = match.start(), match.end()
            for gear in gears.intersection(border(r, c0, c1)):
                gear_digits[gear].append(number)   
    return sum(ns[0] * ns[1] for ns in gear_digits.values() if len(ns) == 2)


solution = part_2()
assert solution == 84584891
print(solution)
