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
            case "swap": instruction = cmd, "letter", args[1], args[4]
            case "rotate" if args[-1].startswith("step"):
                instruction = cmd, args[0], int(args[-2])
            case "rotate": instruction = cmd, args[-1]
            case "reverse": instruction = cmd, int(args[-3]), int(args[-1])
            case "move": instruction = cmd, int(args[-4]), int(args[-1])
        instructions.append(instruction)
if EXAMPLE:
    pprint(instructions)
START = list("abcde" if EXAMPLE else "abcdefgh")

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

LENGTH = len(START)
SHIFT = {i: (i + (1 if i < 4 else 2)) % LENGTH for i in range(LENGTH)}
SHIFT_REV = {(i + n) % LENGTH: -n % LENGTH for i, n in SHIFT.items()}


def step(state, cmd, args):
    match cmd:
        case "swap" if args[0] == "position":
            i, j = args[1], args[2]
            state[i], state[j] = state[j], state[i]
        case "swap":
            i, j = state.index(args[1]), state.index(args[2])
            state[i], state[j] = state[j], state[i]
        case "rotate" if (d := args[0]) in ("left", "right"):
            shift = -args[1] if d == "right" else args[1]
            state = [state[(i + shift) % LENGTH] for i in range(LENGTH)]
        case "rotate" if args[0] == "rev":
            shift = SHIFT_REV[state.index(args[1])]
            state = [state[(i - shift) % LENGTH] for i in range(LENGTH)]
        case "rotate":
            shift = SHIFT[state.index(args[0])]
            state = [state[(i - shift) % LENGTH] for i in range(LENGTH)]
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


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


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


def reverse(instruction):
    cmd, *args = instruction
    match cmd:
        case "rotate" if (d := args[0]) in ("left", "right"):
            args = "left" if d == "right" else "right", args[1]
        case "rotate": args = "rev", args[0]
        case "move": args = args[1], args[0]
    return cmd, args


def part_2(instructions, scrambled):
    state = list(scrambled)
    for instruction in reversed(instructions):
        cmd, args = reverse(instruction)
        state = step(state, cmd, args)
    return "".join(state)


print(solution := part_2(instructions, "decab" if EXAMPLE else "fbgdceah"))
assert solution == ("abcde" if EXAMPLE else "bcfaegdh")
