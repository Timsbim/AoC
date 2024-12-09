# --------------------------------------------------------------------------- #
#    Day 21                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 21
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

with open(file_name, "r") as file:
    instructions = []
    for line in file:
        cmd, *args = line.split()
        match cmd:
            case "swap" if args[0] == "position":
                instruction = cmd, "position", int(args[1]), int(args[4])
            case "swap":
                instruction = cmd, "letter", args[1], args[4]
            case "rotate" if args[-1].startswith("step"):
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
START = list("abcde" if EXAMPLE else "abcdefgh")

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #



# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def step(state, cmd, args):
    match cmd:
        case "swap" if args[0] == "position":
            i, j = args[1], args[2]
            state[i], state[j] = state[j], state[i]
        case "swap":
            a, b = args[1], args[2]
            i, j = state.index(args[1]), state.index(args[2])
            state[i], state[j] = state[j], state[i]
        case "rotate" if (d := args[0]) in ("left", "right"):
            length, shift = len(state), -args[1] if d == "right" else args[1]
            state = [
                state[i] for i in ((i + shift) % length for i in range(length))
            ]
        case "rotate":
            length, shift = len(state), state.index(args[1]) + 1
            if shift >= 5:
                shift += 1
            state = [
                state[i] for i in ((i - shift) % length for i in range(length))
            ]            
        case "reverse":
            start, stop = args
            rev = reversed(state[start:stop+1])
            for i, c in enumerate(rev, start):
                state[i] = c
        case "move":
            i, j = args
            a, state = state[i], state[:i] + state[i+1:]
            state = state[:j] + [a] + state[j:]
    return state


def part_1(instructions):
    state = START.copy()
    for cmd, *args in instructions:
        state = step(state, cmd, args)
    return "".join(state)


print(solution := part_1(instructions))
assert solution == ("decab" if EXAMPLE else "gbhafcde")

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return None


print(solution := part_2())
#assert solution == (if EXAMPLE else)
