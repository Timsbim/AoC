# --------------------------------------------------------------------------- #
#    Day 17                                                                   #
# --------------------------------------------------------------------------- #
from itertools import product
from pprint import pprint

import networkx as nx


DAY = 17
EXAMPLE = True

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
    grid = file.read().splitlines()
    losses = [list(map(int, row)) for row in grid]
if EXAMPLE:
    pprint(grid)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

HEIGHT, WIDTH = len(grid), len(grid[0])
STOP_Y, STOP_X = HEIGHT - 1, WIDTH - 1

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def steps(y, x, count, direction):
    if direction == ">":
        if 0 < y:
            yield y - 1, x, 1, "^"
        if x < STOP_X and count < 3:
            yield y, x + 1, count + 1, ">"
        if y < STOP_Y:
            yield y + 1, x, 1, "v"

    elif direction == "v":
        if x < STOP_X:
            yield y, x + 1, 1, ">"
        if y < STOP_Y and count < 3:
            yield y + 1, x, count + 1, "v"
        if 0 < x:
            yield y, x - 1, 1, "<"

    elif direction == "<":
        if y < STOP_Y:
            yield y + 1, x, 1, "v"
        if 0 < x and count < 3:
            yield y, x - 1, count + 1, "<"
        if 0 < y:
            yield y - 1, x, 1, "^"

    else:
        if 0 < x:
            yield y, x - 1, 1, "<"
        if 0 < y and count < 3:
            yield y - 1, x, count + 1, "^"
        if x < STOP_X:
            yield y, x + 1, 1, ">"


def part_1(grid, losses):
    vertices = (
        (y, x, count, direction)
        for y, x in product(range(HEIGHT), range(WIDTH))
        for count in (1, 2, 3)
        for direction in (">", "v", "<", "^")
    )
    edges = (
        ((y0, x0, c0, d0), (y1, x1, c1, d1), {"loss": losses[y1][x1]})
        for y0, x0, c0, d0 in vertices
        for y1, x1, c1, d1 in steps(y0, x0, c0, d0)
    )
    G = nx.DiGraph()
    G.add_edges_from(edges)
    
    starts = (0, 0, 1, ">"), (0, 0, 1, "v")
    ends = (
        (STOP_Y, STOP_X, count, direction)
        for count in (1, 2, 3)
        for direction in (">", "v")
    )
    paths = (
        nx.shortest_path(G, start, end, "loss")
        for start, end in product(starts, ends)
    )
    return min(sum(losses[y][x] for y, x, *_ in path[1:]) for path in paths)


solution = part_1(grid, losses)
assert solution == (102 if EXAMPLE else 635)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def steps_ultra(y, x, count, direction):
    if direction == ">":
        if 0 < y and 4 <= count:
            yield y - 1, x, 1, "^"
        if x < STOP_X and count < 10:
            yield y, x + 1, count + 1, ">"
        if y < STOP_Y and 4 <= count:
            yield y + 1, x, 1, "v"

    elif direction == "v":
        if x < STOP_X and 4 <= count:
            yield y, x + 1, 1, ">"
        if y < STOP_Y and count < 10:
            yield y + 1, x, count + 1, "v"
        if 0 < x and 4 <= count:
            yield y, x - 1, 1, "<"

    elif direction == "<":
        if y < STOP_Y and 4 <= count:
            yield y + 1, x, 1, "v"
        if 0 < x and count < 10:
            yield y, x - 1, count + 1, "<"
        if 0 < y and 4 <= count:
            yield y - 1, x, 1, "^"

    else:
        if 0 < x and 4 <= count:
            yield y, x - 1, 1, "<"
        if 0 < y and count < 10:
            yield y - 1, x, count + 1, "^"
        if x < STOP_X and 4 <= count:
            yield y, x + 1, 1, ">"


def part_2(grid, losses):
    vertices = (
        (y, x, count, direction)
        for y, x in product(range(HEIGHT), range(WIDTH))
        for count in range(1, 11)
        for direction in (">", "v", "<", "^")
    )
    edges = (
        ((y0, x0, c0, d0), (y1, x1, c1, d1), {"loss": losses[y1][x1]})
        for y0, x0, c0, d0 in vertices
        for y1, x1, c1, d1 in steps_ultra(y0, x0, c0, d0)
    )
    G = nx.DiGraph()
    G.add_edges_from(edges)
    
    starts = (0, 0, 1, ">"), (0, 0, 1, "v")
    ends = (
        (STOP_Y, STOP_X, count, direction)
        for count in range(4, 11)
        for direction in (">", "v")
    )
    minimum = float("inf")
    for start, end in product(starts, ends):
        try:
            path = nx.shortest_path(G, start, end, "loss")
            path_loss = sum(losses[y][x] for y, x, *_ in path[1:])
            minimum = min(minimum, path_loss)
        except nx.exception.NetworkXNoPath:
            pass
    return minimum


def steps_ultra(y, x, count, direction):
    if direction == ">":
        if 3 < y and 4 <= count:
            yield y - 4, x, 4, "^"
        if x < STOP_X and count < 10:
            yield y, x + 1, count + 1, ">"
        if y <= STOP_Y - 4 and 4 <= count:
            yield y + 4, x, 4, "v"

    elif direction == "v":
        if x <= STOP_X - 4 and 4 <= count:
            yield y, x + 4, 4, ">"
        if y < STOP_Y and count < 10:
            yield y + 1, x, count + 1, "v"
        if 3 < x and 4 <= count:
            yield y, x - 4, 4, "<"

    elif direction == "<":
        if y <= STOP_Y - 4 and 4 <= count:
            yield y + 4, x, 4, "v"
        if 0 < x and count < 10:
            yield y, x - 1, count + 1, "<"
        if 3 < y and 4 <= count:
            yield y - 4, x, 4, "^"

    else:
        if 3 < x and 4 <= count:
            yield y, x - 4, 4, "<"
        if 0 < y and count < 10:
            yield y - 1, x, count + 1, "^"
        if x < STOP_X - 4 and 4 <= count:
            yield y, x + 4, 4, ">"


def loss(y0, x0, y1, x1):
    if y1 - y0 == 4:
        return sum(losses[y0 + i][x1] for i in range(1, 5))
    if y0 - y1 == 4:
        return sum(losses[y0 - i][x1] for i in range(1, 5))
    if x1 - x0 == 4:
        return sum(losses[y1][x0 + i] for i in range(1, 5))
    if x0 - x1 == 4:
        return sum(losses[y1][x0 - i] for i in range(1, 5))
    if y1 - y0 == 3:
        return sum(losses[y0 + i][x1] for i in range(0, 4))
    if y0 - y1 == 3:
        return sum(losses[y0 - i][x1] for i in range(0, 4))
    if x1 - x0 == 3:
        return sum(losses[y1][x0 + i] for i in range(0, 4))
    if x0 - x1 == 3:
        return sum(losses[y1][x0 - i] for i in range(0, 4))
    return losses[y1][x1]


def part_2(grid, losses):
    vertices = (
        (y, x, count, direction)
        for y, x in product(range(len(grid)), range(len(grid[0])))
        for count in range(4, 11)
        for direction in (">", "v", "<", "^")
    )
    edges = (
        ((y0, x0, c0, d0), (y1, x1, c1, d1), {"loss": loss(y0, x0, y1, x1)})
        for y0, x0, c0, d0 in vertices
        for y1, x1, c1, d1 in steps_ultra(y0, x0, c0, d0)
    )
    G = nx.DiGraph()
    G.add_edges_from(edges)
    
    starts = (0, 3, 4, ">"), (3, 0, 4, "v")
    first_losses = {
        (0, 3, 4, ">"): losses[0][1] + losses[0][2] + losses[0][3],
        (3, 0, 4, "v"): losses[1][0] + losses[2][0] + losses[3][0] 
    }
    ends = (
        (STOP_Y, STOP_X, count, direction)
        for count in range(4, 11)
        for direction in (">", "v")
    )
    minimum = float("inf")
    for start, end in product(starts, ends):
        try:
            path = nx.shortest_path(G, start, end, "loss")
            path_loss = sum(G[e0][e1]["loss"] for e0, e1 in zip(path, path[1:]))
            minimum = min(minimum, path_loss + first_losses[path[0]])
        except nx.exception.NetworkXNoPath:
            pass
    return minimum


solution = part_2(grid, losses)
assert solution == (94 if EXAMPLE else 734)
print(solution)
