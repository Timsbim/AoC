# --------------------------------------------------------------------------- #
#    Day 18                                                                   #
# --------------------------------------------------------------------------- #
from functools import partial
from itertools import product


DAY = 18
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    grid = list(map(list, file.read().splitlines()))
    #grid = list(reversed(grid))
if EXAMPLE:
    print("\n" + "\n".join("".join(row) for row in grid), end="\n\n")

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def print_grid(grid):
    print("\n" + "\n".join("".join(row) for row in grid), end="\n\n")


def neighbours(limit_y, limit_x, y0, x0):
    # Assumption: gird sides have at least size 3
    if 0 < y0:
        if 0 < x0:
            if y0 < limit_y:
                if x0 < limit_x:  # Inner point: full circle around it
                    y1, x1 = y0 + 1, x0 + 1
                    yield (y1, x0); yield (y1, x1); yield (y0, x1)
                    y1 = y0 - 1
                    yield (y1, x1); yield (y1, x0)
                    x1 = x0 - 1
                    yield (y1, x1); yield (y0, x1); yield (y0 + 1, x1)
                else:  # x0 == limit_x
                    y1 = y0 - 1
                    yield (y1, limit_x)
                    x1 = limit_x - 1
                    yield (y1, x1); yield (y0, x1)
                    y1 = y0 + 1
                    yield (y1, x1); yield (y1, limit_x)
            else:  # y0 == limit_y
                if x0 < limit_x:
                    x1 = x0 + 1
                    yield (limit_y, x1)
                    y1 = limit_y - 1
                    yield (y1, x1); yield (y1, x0)
                    x1 = x0 - 1
                    yield (y1, x1); yield (limit_y, x1)
                else:  # y0 == limit_y and x0 == limit_x
                    y1 = limit_y - 1
                    yield (y1, limit_x);
                    x1 = limit_x - 1
                    yield (y1, x1); yield (limit_y, x1)
        else:  # x0 == 0
            if y0 < limit_y:
                y1 = y0 + 1
                yield (y1, 0); yield (y1, 1); yield (y0, 1)
                y1 = y0 - 1
                yield (y1, 1); yield (y1, 0)
            else:  # x0 == 0 and y0 == limit_y
                y1 = limit_y - 1
                yield (limit_y, 1); yield (y1, 1); yield (y1, 0)
    else:  # y0 == 0
        if 0 < x0:
            if x0 < limit_x:
                x1 = x0 - 1
                yield (0, x1); yield (1, x1); yield (1, x0)
                x1 = x0 + 1
                yield (1, x1); yield (0, x1)
            else:  # y0 == 0 and x0 == limit_x
                x1 = limit_x - 1
                yield (0, x1); yield (1, x1); yield (1, limit_x)
        else:  # y0 == 0 and  x0 == 0
            yield (1, 0); yield (1, 1); yield (0, 1)


def test_neighbours():
    assert [*neighbours(10, 10, 5, 5)]   == [(6, 5), (6, 6), (5, 6), (4, 6), (4, 5), (4, 4), (5, 4), (6, 4)]
    assert [*neighbours(10, 10, 0, 0)]   == [(1, 0), (1, 1), (0, 1)]
    assert [*neighbours(10, 10, 10, 0)]  == [(10, 1), (9, 1), (9, 0)]
    assert [*neighbours(10, 10, 10, 10)] == [(9, 10), (9, 9), (10, 9)]
    assert [*neighbours(10, 10, 0, 10)]  == [(0, 9), (1, 9), (1, 10)]
    assert [*neighbours(10, 10, 5, 0)]   == [(6, 0), (6, 1), (5, 1), (4, 1), (4, 0)]
    assert [*neighbours(10, 10, 10, 5)]  == [(10, 6), (9, 6), (9, 5), (9, 4), (10, 4)]
    assert [*neighbours(10, 10, 5, 10)]  == [(4, 10), (4, 9), (5, 9), (6, 9), (6, 10)]
    assert [*neighbours(10, 10, 0, 5)]   == [(0, 4), (1, 4), (1, 5), (1, 6), (0, 6)]


test_neighbours()

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

neighbours = partial(neighbours, len(grid) - 1, len(grid[0]) - 1)


def counting(grid):
    return [
        [
            sum(1 for y, x in neighbours(y0, x0) if grid[y][x] == "#")
            for x0, lamp in enumerate(row)
        ]
        for y0, row in enumerate(grid)
    ]


def one_step(grid, exclude):
    counts = counting(grid)
    for y, row in enumerate(grid):
        for x, lamp in enumerate(row):
            if (y, x) in exclude:
                continue
            count = counts[y][x]
            if lamp == "#":
                if count != 2 and count != 3:
                    grid[y][x] = "."
            else:
                if count == 3:
                    grid[y][x] = "#"


def stepping(grid, steps, exclude=set()):
    for _ in range(steps):
        one_step(grid, exclude)
        if EXAMPLE:
            print_grid(grid)


def part_1(grid, steps):
    grid = [row.copy() for row in grid]
    stepping(grid, steps)
    range_y, range_x = range(len(grid)), range(len(grid[0]))
    return sum(1 for y, x in product(range_y, range_x) if grid[y][x] == "#")


solution = part_1(grid, 4 if EXAMPLE else 100)
assert solution == (4 if EXAMPLE else 1061)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(grid, steps):
    grid = [row.copy() for row in grid]
    corners = set(product((0, len(grid) - 1), (0, len(grid[0]) - 1)))
    for y, x in corners:
        grid[y][x] = "#"
    stepping(grid, steps, corners)
    range_y, range_x = range(len(grid)), range(len(grid[0]))
    return sum(1 for y, x in product(range_y, range_x) if grid[y][x] == "#")


solution = part_2(grid, 5 if EXAMPLE else 100)
assert solution == (17 if EXAMPLE else 1006)
print(solution)
