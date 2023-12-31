# --------------------------------------------------------------------------- #
#    Day 1                                                                    #
# --------------------------------------------------------------------------- #
import re


DAY = 1
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
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    re_digits = re.compile(r"\d")
    with open(file_name, "r") as file:
        s = 0
        for line in file:
            digits = re_digits.findall(line)
            s += int(digits[0] + digits[-1])
    return s


solution = part_1()
if not EXAMPLE:
    assert solution == 54601
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    DIGITS = {
        "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9"
    }
    inner_pattern = "|".join(["\d"] + list(DIGITS.keys()))
    re_digits = re.compile(f"(?=({inner_pattern}))")
    with open(file_name, "r") as file:
        s = 0
        for line in file:
            digits = re_digits.findall(line)
            first = DIGITS.get(digits[0], digits[0])
            last = DIGITS.get(digits[-1], digits[-1])
            s += int(first + last)
    return s


solution = part_2()
assert solution == (281 if EXAMPLE else 54078)
print(solution)
