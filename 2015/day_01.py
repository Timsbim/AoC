# --------------------------------------------------------------------------- #
#    Day 1                                                                    #
# --------------------------------------------------------------------------- #

DAY = 1
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    parenthesis = file.read().rstrip()
if EXAMPLE:
    print(parenthesis)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

solution = sum(1 if p == "(" else -1 for p in parenthesis)
if not EXAMPLE:
    assert solution == 232
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    floor = 0
    for n, p in enumerate(parenthesis, start=1):
        floor += 1 if p == "(" else -1
        if floor == -1:
            return n


solution = part_2()
if not EXAMPLE:
    assert solution == 1783
print(solution)
