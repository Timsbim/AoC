# Day 15
from pprint import pprint
from itertools import product
from functools import partial


DAY = 15
EXAMPLE = True


# Preparation
file_name = f"2021/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"


# Reading input
with open(file_name, "r") as file:
    levels_input = [
        [int(n) for n in line.strip()] for line in file
    ]

print("\nInput:")
# pprint(levels)
print(
    f"rows: {len(levels_input)},", 
    f"columns: {len(levels_input[0])}"
)


# Helper functions


def adjacents(i, j, levels):
    rows, cols = len(levels) - 1, len(levels[0]) - 1
    return (
        (
            {(i, k) for k in range(max(0, j - 1), min(cols, j + 1) + 1)}
            | {(k, j) for k in range(max(0, i - 1), min(rows, i + 1) + 1)}
        ) - {(i, j)}
    )


# Part 1
print("\nPart 1:")

levels = [level[:] for level in levels_input]


def evaluate(dict_, p):
    return dict_[p]


rows, cols = len(levels), len(levels[0])
value = (rows + cols - 1) * 9
dist = dict.fromkeys(product(range(rows), range(cols)), value)
dist[0, 0] = 0
target = (rows - 1, cols - 1)
key = partial(evaluate, dist)
unvisited = set(dist.keys())
while unvisited:
    p = min(unvisited, key=key)
    if p == target:
        break
    unvisited.discard(p)
    for i, j in adjacents(*p, levels) & unvisited:
        new_dist = dist[p] + levels[i][j]
        if new_dist < dist[i, j]:
            dist[i, j] = new_dist

print(f"Minimal risk: {dist[target]}")

"""
import networkx as nx

levels = [level[:] for level in levels_input]
rows, cols = len(levels), len(levels[0])

G = nx.DiGraph()
G.add_edges_from(
    (
        ((k, l), (i, j), {"weight": levels[i][j]})
        for i, j in set(product(range(rows), range(cols)))
        for k, l in adjacents(i, j, levels)
    )
)
# print(G.edges())
print(
    nx.shortest_path_length(G, (0, 0), (rows - 1, cols - 1), weight="weight")
)

# Result: 707
"""

# Part 2
print("\nPart 2:")

rows, cols = len(levels_input), len(levels_input[0])
levels = [level[:] + [0] * 4 * cols for level in levels_input]
for level in levels:
    for j in range(cols, 5 * cols):
        value = level[j - cols] + 1
        if value == 10:
            value = 1
        level[j] = value
for i in range(rows, 5 * rows):
    levels.append(
        [n + 1 if n < 9 else 1 for n in levels[i - rows]]
    )

rows, cols = len(levels), len(levels[0])
value = (rows + cols - 1) * 9
dist = dict.fromkeys(product(range(rows), range(cols)), value)
dist[0, 0] = 0
target = (rows - 1, cols - 1)
key = partial(evaluate, dist)
unvisited = set(dist.keys())
while unvisited:
    p = min(unvisited, key=key)
    if p == target:
        break
    unvisited.discard(p)
    for i, j in adjacents(*p, levels) & unvisited:
        new_dist = dist[p] + levels[i][j]
        if new_dist < dist[i, j]:
            dist[i, j] = new_dist

print(f"Minimal risk: {dist[target]}")

"""
import nextworkx as nx

rows, cols = len(levels), len(levels[0])
G.add_edges_from(
    (
        ((k, l), (i, j), {"weight": levels[i][j]})
        for i, j in set(product(range(rows), range(cols)))
        for k, l in adjacents(i, j, levels)
    )
)
# print(G.edges())
print(
    nx.shortest_path_length(G, (0, 0), (rows - 1, cols - 1), weight="weight")
)

# Result: 2942
"""
