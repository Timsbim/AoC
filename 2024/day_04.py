# --------------------------------------------------------------------------- #
#    Day 4                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 4
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
    lines = [line.rstrip() for line in file]
if EXAMPLE:
    pprint(lines)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def count(line):
    return line.count("XMAS") + line.count("SAMX")


def part_1(lines):
    rows, cols = len(lines), len(lines[0])
    return (
        sum(count(line) for line in lines)
        + sum(count("".join(line)) for line in zip(*lines))
        + sum(
            count("".join(lines[d+c][c] for c in range(min(rows - d, cols))))
            for d in range(rows)
        )
        + sum(
            count("".join(lines[r][r+d] for r in range(min(cols - d, rows))))
            for d in range(1, cols)
        )
        + sum(
            count("".join(lines[d-c][c] for c in range(min(d + 1, cols))))
            for d in range(rows)
        )
        + sum(
            count("".join(lines[r][d-r] for r in range(rows - 1, max(-1, d - cols), -1)))
            for d in range(rows, rows + cols - 1)
        )
    )


print(solution := part_1(lines))
assert solution == (18 if EXAMPLE else 2646)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(lines):
    rows, cols = len(lines), len(lines[0])
    count, ms = 0, {"M", "S"}
    return sum(
        lines[r][c] == "A"
            and {lines[r-1][c-1], lines[r+1][c+1]} == ms
            and {lines[r-1][c+1], lines[r+1][c-1]} == ms
        for r in range(1, rows - 1)
        for c in range(1, cols - 1)
    )


print(solution := part_2(lines))
assert solution == (9 if EXAMPLE else 2000)
