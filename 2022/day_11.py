# --------------------------------------------------------------------------- #
#    Day 11                                                                   #
# --------------------------------------------------------------------------- #

from functools import partial
from operator import add, mul

DAY = 11
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def operation(op, right):
    if op == "+":
        return partial(add, int(right))
    else:
        if right == "old":
            return lambda o: o * o
        else:
            return partial(mul, int(right))


def get_monkeys(file_name):
    monkeys = {}
    with open(file_name, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Monkey"):
                n = int(line[line.rfind(" "):-1])
                monkey = monkeys.setdefault(n, {"inspections": 0})
            elif line.startswith("Starting items:"):
                numbers = list(map(int, line[line.rfind(":") + 1:].split(", ")))
                monkey["items"] = numbers
            elif line.startswith("Operation:"):
                op, right = line[line.rfind("= old") + 5:].split()
                monkey["op"] = operation(op, right)
            elif line.startswith("Test:"):
                number = int(line[line.rfind(" "):])
                test = monkey.setdefault("test", {"div_by": number})
            elif line.startswith("If true:"):
                test[True] = int(line[line.rfind(" "):])
            elif line.startswith("If false:"):
                test[False] = int(line[line.rfind(" "):])
    return monkeys    

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def inspections(monkeys, rounds, part=1):
    if part != 1:
        max_level = 1
        for monkey in monkeys.values():
            max_level *= monkey["test"]["div_by"]
    for _ in range(rounds):
        for monkey in monkeys.values():
            monkey["inspections"] += len(monkey["items"])
            test = monkey["test"]
            for item in monkey["items"]:
                if part == 1:
                    level = monkey["op"](item) // 3
                else:
                    level = monkey["op"](item) % max_level
                res = level % test["div_by"] == 0
                monkeys[test[res]]["items"].append(level)
            monkey["items"] = []            


def top_inspections(monkeys):
    n, m = sorted(m["inspections"] for m in monkeys.values())[-2:]
    return n * m
            
# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

monkeys = get_monkeys(file_name)
inspections(monkeys, 20)
print(top_inspections(monkeys))  # 54036
    
# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

monkeys = get_monkeys(file_name)
inspections(monkeys, 10_000, part=2)
print(top_inspections(monkeys))  # 13237873355
