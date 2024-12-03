# --------------------------------------------------------------------------- #
#    Day 3                                                                    #
# --------------------------------------------------------------------------- #
import re
from pprint import pprint


DAY = 3
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

if EXAMPLE:
    memory = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
else:
    with open(file_name, "r") as file:
        memory = file.read().rstrip()

if EXAMPLE:
    pprint(memory)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

RE_MUL = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def part_1(memory):
    return sum(int(m[1]) * int(m[2]) for m in RE_MUL.finditer(memory))


print(solution := part_1(memory))
assert solution == (161 if EXAMPLE else 157621318)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(memory):
    re_flip = re.compile(r"(do\(\)|don't\(\))")
    res, mul = 0, True
    for part in re_flip.split(memory):
        if part == "do()":
            mul = True
        elif part == "don't()":
            mul = False
        elif mul:
            res += part_1(part)
    return res


print(solution := part_2(memory))
assert solution == (48 if EXAMPLE else 79845780)
