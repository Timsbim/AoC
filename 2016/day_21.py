# --------------------------------------------------------------------------- #
#    Day 21                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 21
EXAMPLE = True

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

with open(file_name, "r") as file:
    instructions = []
    for line in file:
        cmd, *args = line.split()
        match cmd:
            case "swap" if args[0] == "position":
                instruction = cmd, "position", int(args[1]), int(args[4])
            case "swap":
                instruction = cmd, "letter", args[1], args[4]
            case "rotate" if args[-1] == "steps":
                instruction = cmd, args[0], int(args[-2])
            case "rotate":
                instruction = cmd, "letter", args[-1]
            case "reverse":
                instruction = cmd, int(args[-3]), int(args[-1])
            case "move":
                instruction = cmd, int(args[-4]), int(args[-1])
        instructions.append(instruction)
if EXAMPLE:
    pprint(instructions)
START = "abcde" if EXAMPLE else "abcdefgh"


# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #



# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    return None


print(solution := part_1())
#assert solution == ("decab" if EXAMPLE else "")

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return None


print(solution := part_2())
#assert solution == (if EXAMPLE else)
