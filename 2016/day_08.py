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

file_name = f"2016/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

COLS, ROWS = (7, 3) if EXAMPLE else (50, 6)

re_del = re.compile(r"x|y|=|by")
with open(file_name, "r") as file:
    instructions = []
    for line in file:
        row = re_del.sub(" ", line).split()
        row[-2], row[-1] = int(row[-2]), int(row[-1])
        instructions.append(tuple(row))
    instructions = tuple(instructions)
if EXAMPLE:
    pprint(instructions)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def print_screen(screen):
    print("\n", "\n".join("".join(row) for row in screen), sep="")


def set_screen(instructions):
    screen = [["."] * COLS for _ in range(ROWS)]
    for cmd, *params in instructions:
        if cmd == "rect":
            cols, rows = params
            for r in range(rows):
                for c in range(cols):
                    screen[r][c] = "#"
        else:
            axis, n, shift = params
            if axis == "row":
                row_new = ["."] * COLS
                for c in range(COLS):
                    if screen[n][c] == "#":
                        row_new[(c + shift) % COLS] = "#"
                screen[n] = row_new
            else:
                col_new = ["."] * ROWS
                for r in range(ROWS):
                    if screen[r][n] == "#":
                        col_new[(r + shift) % ROWS] = "#"
                for r, char in enumerate(col_new):
                    screen[r][n] = char
    return screen


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(instructions):
    screen = set_screen(instructions)
    if EXAMPLE:            
        print_screen(screen)
    return sum(char == "#" for row in screen for char in row)


print(solution := part_1(instructions))
assert solution == (6 if EXAMPLE else 121)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(instructions):
    print_screen(set_screen(instructions))
    return "RURUCEOEIL"


print(solution := part_2(instructions))
