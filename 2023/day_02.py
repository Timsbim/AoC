# --------------------------------------------------------------------------- #
#    Day 2                                                                    #
# --------------------------------------------------------------------------- #
import re
from math import prod


DAY = 2
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

re_cube = re.compile(r"(\d+) ([^,;\s]+)")

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

LIMITS = {"red": 12, "green": 13, "blue": 14}

with open(file_name, "r") as file:
    sum_ids = sum(
        ID for ID, line in enumerate(file, start=1)
        if all(int(n) <= LIMITS[col] for n, col in re_cube.findall(line))
    )

print(sum_ids)  # 2439

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

sum_powers = 0
with open(file_name, "r") as file:
    for line in file:
        mins = {"red": 0, "green": 0, "blue": 0}
        for num, color in re_cube.findall(line):
            if (num := int(num)) > mins[color]:
                mins[color] = num
        sum_powers += prod(mins.values())

print(sum_powers)  # 63711
