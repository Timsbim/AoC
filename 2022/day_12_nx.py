# --------------------------------------------------------------------------- #
#    Day 12                                                                   #
# --------------------------------------------------------------------------- #

import networkx as nx
from itertools import product
from string import ascii_lowercase as letters

DAY = 12
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_map(file_name):
    with open(file_name, "r") as file:
        heights = file.read().strip()
    width = heights.index("\n")
    heights = heights.replace("\n", "")
    start, end = heights.index("S"), heights.index("E")
    levels = dict({l: n for n, l in enumerate(letters)}, S=0, E=25)
    return divmod(start, width), divmod(end, width), [
        [levels[l] for l in heights[i:i + width]]
        for i in range(0, len(heights), width)
    ]

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def neighbours(edge, length, width):
    i, j = edge
    if 0 < j:
        yield i, j - 1
    if j < width - 1:
        yield i, j + 1
    if 0 < i:
        yield i - 1, j
    if i < length - 1:
        yield i + 1, j


def nodes(heights):
    length, width = len(heights), len(heights[0])
    yield from product(range(length), range(width))


def build_graph(heights):
    length, width = len(heights), len(heights[0])
    G = nx.DiGraph()
    for i, j in nodes(heights):
        limit = heights[i][j] + 1
        G.add_node((i, j))
        G.add_edges_from(
            ((i, j), (k, l))
            for k, l in neighbours((i, j), length, width)
            if heights[k][l] <= limit
        )
    return G
    
# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

start, end, heights = get_map(file_name)
print(nx.shortest_path_length(build_graph(heights), start, end))  # 520

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

start, end, heights = get_map(file_name)
G = build_graph(heights)
min_lengths = []
for i, j in nodes(heights):
    if heights[i][j] == 0:
        try:
            min_lengths.append(nx.shortest_path_length(G, (i, j), end))
        except nx.exception.NetworkXNoPath:
            pass
min_length = min(min_lengths)
print(min_length)  # 508
