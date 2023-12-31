# --------------------------------------------------------------------------- #
#    Day 19                                                                   #
# --------------------------------------------------------------------------- #
from operator import gt, lt
from pprint import pprint
from math import prod


DAY = 19
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    workflows = {}
    for line in file:
        line = line.strip()
        if line == "":
            break
        key, steps = line[:-1].split("{")
        workflow = workflows.setdefault(key, [])
        for step in steps.split(","):
            if ":" not in step:  # Singelton
                workflow.append(step)
            else:
                condition, dest = step.split(":")
                key, op, value = condition[0], condition[1], condition[2:]
                workflow.append((key, op, int(value), dest))
            
    parts = []
    for line in file:
        line = line.strip()[1:-1]
        part = {}
        for step in line.split(","):
            key, value = step.split("=")
            part[key] = int(value)
        parts.append(part)

if EXAMPLE:
    pprint(workflows, sort_dicts=False)
    pprint(parts)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def process(workflows, part):
    funcs = {"<": lt, ">": gt}
    key = "in"
    while key != "A" and key != "R":
        workflow = workflows[key]
        for step in workflow:
            if isinstance(step, tuple):
                key, op, value, dest = step
                if funcs[op](part[key], value):
                    key = dest
                    break
            else:  # Singelton: always last
                key = step

    return key


def part_1(workflows, parts):
    return sum(
        sum(part.values())
        for part in parts
        if process(workflows, part) == "A"
    )


solution = part_1(workflows, parts)
assert solution == (19114 if EXAMPLE else 368964)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def process(workflows):
    finished = []
    process = [("in", {key: (1, 4_000) for key in "xmas"})]
    while process:
        key, part = process.pop()
        for step in workflows[key]:
            if isinstance(step, tuple):
                key, op, value, dest = step
                start, end = part[key]
                if op == "<":
                    if value <= start:
                        continue
                    new_part = dict(part)
                    new_part[key] = start, min(value - 1, end)
                    queue = finished if dest in ("A", "R") else process
                    queue.append((dest, new_part))
                    if end < value:
                        break
                    part[key] = value, end
                elif op == ">":
                    if end <= value:
                        continue
                    new_part = dict(part)
                    new_part[key] = max(start, value + 1), end
                    queue = finished if dest in ("A", "R") else process
                    queue.append((dest, new_part))
                    if value < start:
                        break
                    part[key] = start, value
            else:
                queue = finished if step in ("A", "R") else process
                queue.append((step, part))
    
    return finished


def part_2(workflows):
    return sum(
        prod(end - start + 1 for start, end in part.values())
        for key, part in process(workflows)
        if key == "A"
    )


solution = part_2(workflows)
assert solution == (167409079868000 if EXAMPLE else 127675188176682)
print(solution)
