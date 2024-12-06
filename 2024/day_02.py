# --------------------------------------------------------------------------- #
#    Day 2                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 2
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

with open(file_name, "r") as file:
    reports = tuple(tuple(map(int, line.split())) for line in file)
 
if EXAMPLE:
    pprint(reports)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def is_safe(report):
    slope = report[0] < report[1]
    for a, b in zip(report, report[1:]):
        diff = abs(a - b)
        if diff == 0 or 3 < diff or (a < b) != slope:
            return False
    return True
 

def part_1(reports):
    return sum(is_safe(report) for report in reports)
 

print(solution := part_1(reports))
assert solution == (2 if EXAMPLE else 479)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def is_safe_mod(report):
    for i in range(len(report)):
        report_mod = report[:i] + report[i+1:]
        if is_safe(report_mod):
            return True
    return False
 

def part_2(reports):
    return sum(is_safe_mod(report) for report in reports)
 

print(solution := part_2(reports))
assert solution == (4 if EXAMPLE else 531)
