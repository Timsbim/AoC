# --------------------------------------------------------------------------- #
#    Day 20                                                                   #
# --------------------------------------------------------------------------- #
from collections import deque
from math import lcm
from pprint import pprint


DAY = 20
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

def read_input():
    with open(file_name, "r") as file:
        modules = {}
        for line in file:
            sender, receiver = line.strip().split(" -> ")
            receiver = tuple(receiver.split(", "))
            if sender == "broadcaster":
                modules["broadcaster"] = receiver
            elif sender.startswith("%"):
                modules[sender[1:]] = ["%", "off", receiver]
            elif sender.startswith("&"):
                modules[sender[1:]] = ["&", "low", receiver]

    graph = {}
    for sender, module in modules.items():
        receivers = module if sender == "broadcaster" else module[2]
        for receiver in receivers:
            graph.setdefault(receiver, set()).add(sender)
    for sender, module in modules.items():
        if module[0] == "&":
            module[1] = dict.fromkeys(graph[sender], False)

    if EXAMPLE:
        pprint(modules)

    return modules

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def push_button(modules, counts):
    queue = deque([])
    for receiver in modules["broadcaster"]:
        queue.appendleft(("broadcaster", receiver, "low"))
    counts["low"] += len(modules["broadcaster"]) + 1
    while queue:
        sender, receiver, pulse = queue.pop()
        module = modules.get(receiver)
        if module is None:
            continue
        if module[0] == "%":
            if pulse == "high":
                continue
            if module[1] == "off":
                module[1], pulse = "on", "high"
            else:  # on
                module[1], pulse = "off", "low"
            sender = receiver
            for receiver in module[2]:
                queue.appendleft((sender, receiver, pulse))
            counts[pulse] += len(module[2])
        else:  # &
            memory = module[1]
            memory[sender] = True if pulse == "high" else False
            pulse = "low" if all(memory.values()) else "high"
            sender = receiver
            for receiver in module[2]:
                queue.appendleft((sender, receiver, pulse))
            counts[pulse] += len(module[2])

    return counts


def part_1():
    modules = read_input()
    counts = {"low": 0, "high": 0}
    for _ in range(1_000):
        push_button(modules, counts)
    return counts["low"] * counts["high"]


solution = part_1()
assert solution == (11687500 if EXAMPLE else 703315117)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def push_button(modules):
    ends = []
    n, paths = 0, [("broadcaster", modules["broadcaster"], "low")]
    while paths:
        n += 1
        new_paths = []    
        for sender, receiver, pulse in paths:
            module = modules.get(receiver)
            if module is None:
                continue
            if module[0] == "%":
                if pulse == "high":
                    continue
                if module[1] == "off":
                    module[1], pulse = "on", "high"
                else:  # on
                    module[1], pulse = "off", "low"
                sender = receiver
                for receiver in module[2]:
                    if receiver == "cs":
                        if pulse == "high":
                            ends.append((n, pulse))
                    else:
                        new_paths.append((sender, receiver, pulse))
            else:  # &
                memory = module[1]
                memory[sender] = True if pulse == "high" else False
                pulse = "low" if all(memory.values()) else "high"
                sender = receiver
                for receiver in module[2]:
                    if receiver == "cs":
                        if pulse == "high":
                            ends.append((n, pulse))
                    else:
                        new_paths.append((sender, receiver, pulse))
        paths = new_paths
    
    return ends


def part_2():
    modules = read_input()
    periods = []
    for start_node in "fm", "hv", "kc", "bv":
        nodes, visited = [start_node], {start_node}
        while nodes:
            node = nodes.pop()
            if node in modules and node != "cs":
                neighbours = set(modules[node][2])
                nodes.extend(neighbours - visited)
                visited |= neighbours
        sub_modules = {k: v for k, v in modules.items() if k in visited}
        sub_modules["broadcaster"] = start_node
        
        step = 1
        while True:
            if push_button(sub_modules):
                periods.append(step)
                break
            step += 1 

    return lcm(*periods)


if not EXAMPLE:    
    solution = part_2()
    assert solution == 230402300925361
    print(solution)
