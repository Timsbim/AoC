# --------------------------------------------------------------------------- #
#    Day 5                                                                    #
# --------------------------------------------------------------------------- #
import re
from pprint import pprint


DAY = 5
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
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

VOWELS = "aeiou"

re_3_vowels = re.compile(r"[aeiou][^aeiou]*[aeiou][^aeiou]*[aeiou]")
re_double = re.compile(r"([a-z])\1")
re_excluded = re.compile(r"ab|cd|pq|xy")


def nice(string):
    return (
        bool(re_3_vowels.search(string))
            and bool(re_double.search(string))
            and not bool(re_excluded.search(string))
    )


def part_1():
    return sum(1 for string in strings if nice(string))


solution = part_1()
if not EXAMPLE:
    assert solution == 255
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

re_pair = re.compile(r"([a-z][a-z]).*\1")
re_repeat = re.compile(r"([a-z]).\1")


def nice(string):
    return (bool(re_pair.search(string)) and bool(re_repeat.search(string)))


def part_2():
    return sum(1 for string in strings if nice(string))


solution = part_2()
if not EXAMPLE:
    assert solution == 55
print(solution)
