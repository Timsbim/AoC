# --------------------------------------------------------------------------- #
#    Day 7                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 7
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    instructions = {}
    for line in file:
        op, address = line.rstrip().split(" -> ")
        op = op.split()
        if len(op) == 1:
            cmd, arg = "VAL", op[0]
            instruction = cmd, int(arg) if arg.isdigit() else arg
        elif len(op) == 2:
            cmd, arg = op
            instruction = cmd, int(arg) if arg.isdigit() else arg
        else:
            cmd, arg1, arg2 = op[1], op[0], op[2]
            arg1 = int(arg1) if arg1.isdigit() else arg1
            arg2 = int(arg2) if arg2.isdigit() else arg2
            instruction = cmd, arg1, arg2
        instructions[address] = instruction
if EXAMPLE:
    pprint(instructions)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def reorder_instructions(instructions):
    order = {}
    n, new_addresses = 0, {"a"}
    while new_addresses:
        next_new_addresses = set()
        for address in new_addresses:
            order[address] = -(n := n + 1)
            args = instructions[address][1:]
            next_new_addresses |= {arg for arg in args if type(arg) == str}
        new_addresses = next_new_addresses
    orderd = sorted(order, key=order.get)
    return {addr: instructions[addr] for addr in orderd}


def process_instructions(instructions):
    signals = {}
    for address, op in instructions.items():
        cmd = op[0]
        if cmd == "VAL":
            value = signals.get(op[1], op[1])
        elif cmd == "NOT":
            value = ~signals.get(op[1], op[1])
        elif cmd == "RSHIFT":
            value = signals[op[1]] >> op[2]
        elif cmd == "LSHIFT":
            value = signals[op[1]] << op[2]
        elif cmd == "AND":
            value = signals.get(op[1], op[1]) & signals.get(op[2], op[2])
        else:
            value = signals.get(op[1], op[1]) | signals.get(op[2], op[2])
        signals[address] = value
    return signals["a"]

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

instructions = reorder_instructions(instructions)
solution = process_instructions(instructions)
if not EXAMPLE:
    assert solution == 16076
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

instructions["b"] = "VAL", solution
solution = process_instructions(instructions)
if not EXAMPLE:
    assert solution == 2797
print(solution)
