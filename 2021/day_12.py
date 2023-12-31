# Day 12
from pprint import pprint
from collections import defaultdict


# Reading input
with open("2021/day_12_input.csv", "r") as file:
    edges_input = [tuple(line.strip().split("-")) for line in file]
# pprint(edges_input)


# Part 1
print("Part 1:")

edges = edges_input[:]
graph = defaultdict(set)
for a, b in edges:
    if b != "start":
        graph[a].add(b)
    if a != "start":
        graph[b].add(a)
# pprint(graph)

paths = []
stack = [(["start"], {"start"})]
while stack:
    path, used = stack.pop()
    for node in graph.get(path[-1], []):
        if node not in used:
            new_path, new_used = path[:] + [node], set(used)
            if node == "end":
                paths.append(new_path)
            else:
                if node.islower():
                    new_used.add(node)
                stack.append((new_path, new_used))

# pprint(paths)
num_paths = len(paths)
print(f"Number of paths: {num_paths}")


# Part 2
print("\nPart 2:")

paths = []
stack = [(["start"], {"start"}, True)]
while stack:
    path, used, double = stack.pop()
    for node in graph.get(path[-1], []):
        if node not in used or double:
            new_path = path[:] + [node]
            new_used = set(used)
            new_double = double
            if node == "end":
                paths.append(new_path)
            else:
                if node.islower():
                    if double and node in used:
                        new_double = False
                    else:
                        new_used.add(node)
                stack.append((new_path, new_used, new_double))

# pprint(sorted(paths))
num_paths = len(paths)
print(f"Number of paths: {num_paths}")
