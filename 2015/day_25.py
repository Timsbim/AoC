# --------------------------------------------------------------------------- #
#    Day 25                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 25
EXAMPLE = True

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

# Enter the code at row 3010, column 3019.
ROW, COLUMN = (6, 5) if EXAMPLE else (3010, 3019)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(row, column):
    diag_no = row + column - 1  # Diagonal on which the entry lies
    nth = (diag_no * (diag_no - 1)) // 2 + column  # Corresponding value count
    value = 20151125
    for n in range(2, nth + 1):
        value = (value * 252533) % 33554393
    return value


print(solution := part_1(ROW, COLUMN))
assert solution == (1534922 if EXAMPLE else 8997277)
