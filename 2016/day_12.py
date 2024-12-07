# --------------------------------------------------------------------------- #
#    Day 12                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 12
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

REGISTER = dict(zip("abcd", range(4)))
with open(file_name, "r") as file:
    instructions = []
    for line in file:
        cmd, *args = line.split()
        if cmd == "cpy":
            v, r = args
            instructions.append((cmd, v if v in REGISTER else int(v), r))
        elif cmd == "jnz":
            v, w = args
            instructions.append((cmd, v if v in REGISTER else int(v), int(w)))
        else:
            instructions.append((cmd, args[0]))        
instructions = tuple(instructions)
print("Instructions:")
pprint(instructions)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def run(instructions, c=0):
    p, regs = 0, dict.fromkeys("abcd", 0)
    regs["c"] = c
    while p < len(instructions):
        cmd, *args = instructions[p]
        match cmd:
            case "inc": regs[args[0]] += 1
            case "dec": regs[args[0]] -= 1
            case "cpy": regs[args[1]] = regs.get(args[0], args[0])
            case "jnz":
                if regs.get(args[0], args[0]):
                    p += args[1]
                    continue
        p += 1
    return regs["a"]


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(instructions):
    return run(instructions)


print(solution := part_1(instructions))
assert solution == (42 if EXAMPLE else 317993)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(instructions):
    return run(instructions, c=1)


print(solution := part_2(instructions))
assert solution == (42 if EXAMPLE else 9227647)
