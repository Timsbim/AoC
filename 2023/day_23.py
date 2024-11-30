# --------------------------------------------------------------------------- #
#    Day 23                                                                   #
# --------------------------------------------------------------------------- #
from collections import defaultdict
from pprint import pprint

import heapq


DAY = 23
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
    GRID = file.read().splitlines()
if EXAMPLE:
    print("\n".join(GRID))

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

HEIGHT, WIDTH = len(GRID), len(GRID[0])
STOP_Y, STOP_X = HEIGHT - 1, WIDTH -1
START, STOP = (0, 1), (STOP_Y, STOP_X - 1)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def neighbours(y, x):
    tile = GRID[y][x]
    if tile == ">":
        if GRID[y][x + 1] != "#":
            yield y, x + 1
    elif tile == "v":
        if GRID[y + 1][x] != "#":
            yield y + 1, x
    elif tile == "<":
        if GRID[y][x - 1] != "#":
            yield y, x - 1
    elif tile == "^":
        if GRID[y - 1][x] != "#":
            yield y - 1, x
    else:
        if x < STOP_X and GRID[y][x + 1] != "#":
            yield y, x + 1
        if y < STOP_Y and GRID[y + 1][x] != "#":
            yield y + 1, x
        if 0 < x and GRID[y][x - 1] != "#":
            yield y, x - 1
        if 0 < y and GRID[y - 1][x] != "#":
            yield y - 1, x


def part_1():
    max_dist = float("-inf")
    paths = [(0, START, {START})]
    heapq.heapify(paths)
    while paths:
        dist, pos_0, visited = heapq.heappop(paths)
        dist -= 1
        for pos_1 in neighbours(*pos_0):
            if pos_1 in visited:
                continue
            if pos_1 == STOP:
                max_dist = max(max_dist, abs(dist))
            else:
                heapq.heappush(paths, (dist, pos_1, visited | {pos_1}))
    
    return max_dist


solution = part_1()
assert solution == (94 if EXAMPLE else 2310)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def neighbours(y, x):
    if x < STOP_X and GRID[y][x + 1] != "#":
        yield y, x + 1
    if y < STOP_Y and GRID[y + 1][x] != "#":
        yield y + 1, x
    if 0 < x and GRID[y][x - 1] != "#":
        yield y, x - 1
    if 0 < y and GRID[y - 1][x] != "#":
        yield y - 1, x


def build_graph():
    valid = {".", ">", "v", "<", "^"}
    non_pipes = {
        (y, x)
        for y, row in enumerate(GRID)
        for x, char in enumerate(row)
        if char in valid and len(list(neighbours(y, x))) != 2
    }

    graph = defaultdict(dict)
    visited = set()
    for np_0 in non_pipes:
        paths = [(np_0, 0)]
        while paths:
            p, dist = paths.pop()
            dist += 1
            for np_1 in neighbours(*p):
                if np_1 in visited or np_1 == np_0:
                    continue
                if np_1 in non_pipes:
                    graph[np_0][np_1] = graph[np_1][np_0] = dist
                else:
                    paths.append((np_1, dist))
                    visited.add(np_1)

    return graph


def part_2():
    dists = build_graph()
    graph = {p: set(dist) for p, dist in dists.items()}
    max_dist = float("-inf")
    paths = [(START, {START}, 0)]
    while paths:
        node, visited, dist = paths.pop()
        for next_node in graph[node]:
            if next_node in visited:
                continue
            next_dist = dist + dists[node][next_node]
            if next_node == STOP:
                max_dist = max(max_dist, next_dist)
                continue
            next_visited = visited | {next_node}
            paths.append((next_node, next_visited, next_dist))
    
    return max_dist


solution = part_2()
assert solution == (154 if EXAMPLE else 6738)
print(solution)
