# --------------------------------------------------------------------------- #
#    Day 23                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 23
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/day_23_input.txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    PROGRAMM = []
    for line in file:
        cmd, args = line.strip().split(maxsplit=1)
        args = (
            int(a) if a.startswith("-") or a.startswith("+") else a
            for a in args.split(", ")
        )
        PROGRAMM.append((cmd, *args))

PROGRAMM = tuple(PROGRAMM)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def run(programm, a=0, b=0):
    num_lines = len(programm)
    line, registers = 0, {"a": a, "b": b}
    while line < num_lines:
        cmd, *args = programm[line]
        if cmd == "hlf":
            registers[args[0]] //= 2
            line += 1
        elif cmd == "tpl":
            registers[args[0]] *= 3
            line += 1
        elif cmd == "inc":
            registers[args[0]] += 1
            line += 1
        elif cmd == "jmp":
            line += args[0]
        elif cmd == "jie":
            reg, delta = args
            line += delta if registers[reg] % 2 == 0 else 1
        elif cmd == "jio":
            reg, delta = args
            line += delta if registers[reg] == 1 else 1
        
    return registers

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    return run(PROGRAMM)["b"]


solution = part_1()
assert solution == 307
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return run(PROGRAMM, a=1)["b"]


solution = part_2()
assert solution == 160
print(solution)
