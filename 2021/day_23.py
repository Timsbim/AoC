# --------------------------------------------------------------------------- #
#    Day 23                                                                   #
# --------------------------------------------------------------------------- #

from pprint import pprint

DAY = 23
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

file_name = f"2021/input/day_{DAY:0>2}_part_1.csv"
with open(file_name, "r") as file:
    score = 0
    for line in file:
        line = line.strip()
        if line:
            if line[0].isdigit():
                score += int(line)
print(score) # 16489

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

file_name = f"2021/input/day_{DAY:0>2}_part_2.csv"
with open(file_name, "r") as file:
    score = 0
    for line in file:
        line = line.strip()
        if line:
            if line[0].isdigit():
                score += int(line)
print(score) # 43413
