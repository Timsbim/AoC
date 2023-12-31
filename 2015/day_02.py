# --------------------------------------------------------------------------- #
#    Day 2                                                                    #
# --------------------------------------------------------------------------- #

DAY = 2
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
    dimensions = [tuple(map(int, line.split("x"))) for line in file]
if EXAMPLE:
    print(dimensions)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    paper = 0
    for l, w, h in dimensions:
        s1, s2, s3 = l * w, l * h, w * h
        paper += 2 * (s1 + s2 + s3) + min(s1, s2, s3)
    return paper


solution = part_1()
if not EXAMPLE:
    assert solution == 1598415
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    ribbon = 0
    for l, w, h in dimensions:
        s1, s2 = sorted((l, w, h))[:2]
        ribbon += 2 * (s1 + s2) + l * w * h
    return ribbon


solution = part_2()
if not EXAMPLE:
    assert solution == 3812909
print(solution)
