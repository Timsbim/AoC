# --------------------------------------------------------------------------- #
#    Day 8                                                                    #
# --------------------------------------------------------------------------- #
import re
from pprint import pprint


DAY = 8
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    strings = file.read().splitlines()
if EXAMPLE:
    pprint(strings)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

re_clean = re.compile(r'\\\\|\\x[\da-f][\da-f]|\\"')


def clean(string):
    return re_clean.sub('1', string) 

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    num = 0
    for string in strings:
        string_clean = clean(string).strip('"') 
        num += len(string) - len(string_clean)
    return num


solution = part_1()
if not EXAMPLE:
    assert solution == 1342
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    num = 0
    for string in strings:
        string_dirty = string.replace('\\', '\\\\').replace('\"', '\\"')
        num += len(string_dirty) + 2 - len(string)
    return num


solution = part_2()
if not EXAMPLE:
    assert solution == 2074
print(solution)
