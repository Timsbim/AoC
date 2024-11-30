# --------------------------------------------------------------------------- #
#    Day 25                                                                   #
# --------------------------------------------------------------------------- #
from itertools import combinations
from pprint import pprint


DAY = 25
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    GRAPH = {}
    for line in file:
        node, nodes = line.strip().split(": ")
        nodes = nodes.split(" ")
        GRAPH.setdefault(node, set()).update(nodes)
        for n in nodes:
            GRAPH.setdefault(n, set()).add(node)

if EXAMPLE:
    pprint(GRAPH)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def components(graph):
    counts = []

    length = len(graph)
    visited = set()
    while len(visited) < length:
        node, nodes = graph.popitem()
        component = set(nodes) | {node}
        while nodes:
            next_nodes = set()
            for node_0 in nodes:
                nodes_1 = graph.pop(node_0)
                for node_1 in nodes_1:
                    if node_1 not in component:
                        next_nodes.add(node_1)
            component |= next_nodes
            nodes = next_nodes
        visited |= component
        counts.append(len(component))
    
    return counts


def part_1(cuts=None):
    edges = {
        (n0, n1)
        for n0, n1 in combinations(GRAPH, r=2)
        if n1 in GRAPH[n0]
    }
    if cuts is None:
        cuts = combinations(edges, r=3)
    for cut in cuts:
        cut = set(cut)
        graph = {}
        for n0, nodes in GRAPH.items():
            for n1 in nodes:
                if (n0, n1) not in cut and (n1, n0) not in cut:
                    graph.setdefault(n0, set()).add(n1)
                    graph.setdefault(n1, set()).add(n0)
        
        comps = components(graph)
        if len(comps) == 2:
            n, m = comps
            return n * m


solution = (
    part_1()
    if EXAMPLE else
    part_1([(("ljm", "sfd"), ("gst", "rph"), ("jkn", "cfn"))])
)
assert solution == (54 if EXAMPLE else 596376)
print(solution)
