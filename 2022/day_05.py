# --------------------------------------------------------------------------- #
#    Day 5                                                                    #
# --------------------------------------------------------------------------- #

import re
from itertools import zip_longest

DAY = 5
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    # First part - the stacks
    rows = []
    for line in file:
        line = line.rstrip()
        if "[" not in line:
            break
        row = []    
        for i in range(0, len(line), 4):
            part = line[i:i + 4].strip(" []")
            row.append(part if part else None)
        rows.append(row)
    stacks = [
        list(reversed([crate for crate in stack if crate]))
        for stack in zip_longest(*rows)
    ]

    # Skip blank separator line
    next(file)

    # Second part - the moves
    re_moves = re.compile(r"move (\d+) from (\d+) to (\d+)")
    moves = []
    for line in file:
        count, src, dst = map(int, re_moves.match(line).groups())
        moves.append((count, src - 1, dst - 1))    

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

for count, src, dst in moves:
    stacks[dst].extend(stacks[src].pop() for _ in range(count))
message = "".join(stack[-1] for stack in stacks)
print(message)  # TQRFCBSJJ

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

# Rebuild the stacks
stacks = [
    list(reversed([crate for crate in stack if crate]))
    for stack in zip_longest(*rows)
]

for count, src, dst in moves:
    stacks[dst].extend(reversed([stacks[src].pop() for _ in range(count)]))
message = "".join(stack[-1] for stack in stacks)
print(message)  # RMHFJNVFP
