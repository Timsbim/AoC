# --------------------------------------------------------------------------- #
#    Day 14                                                                   #
# --------------------------------------------------------------------------- #

from itertools import product

DAY = 14
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

def get_rock_paths(file_name):
    with open(file_name, "r") as file:
        paths = []
        for line in file:
            points = line.strip().split(" -> ")
            path = [tuple(map(int, point.split(","))) for point in points]
            paths.append(path)
    return paths

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def fill_path(start, end):
    (s0, s1), (e0, e1) = start, end
    yield from product(
        range(s0, e0 + 1) if s0 < e0 else range(e0, s0 + 1),
        range(s1, e1 + 1) if s1 < e1 else range(e1, s1 + 1)
    )


def get_cave(paths):
    return {
        (i - 500, j): "#"
        for path in paths
        for start, end in zip(path, path[1:])
        for i, j in fill_path(start, end)
    }


def limits(cave):
    min_x = float("inf")
    max_x = max_y = float("-inf")
    for i, j in cave.keys():
        min_x, max_x, max_y = min(min_x, i), max(max_x, i), max(max_y, j)
    return min_x, max_x, max_y


def print_cave(cave, air=" "):
    min_x, max_x, max_y = limits(cave)
    print("\n".join(
        "".join(cave.get((i, j), air) for i in range(min_x, max_x + 1))
        for j in range(0, max_y + 1)
    ))


def drop_sand_in_the_void(cave):
    min_x, max_x, max_y = limits(cave)
    def empty(i, j): return cave.get((i, j)) is None
    num = 0
    while True:
        i, j = 0, 0
        while True:
            if empty(i, j + 1):
                j = j + 1
            elif empty(i - 1, j + 1):
                i, j = i - 1, j + 1
            elif empty(i + 1, j + 1):
                i, j = i + 1, j + 1
            else:
                cave[i, j] = "o"
                num += 1
                break
            if i < min_x or max_x < i or max_y < j:
                return num


def drop_sand_on_the_floor(cave):
    max_y = limits(cave)[-1] + 1
    def empty(i, j): return cave.get((i, j)) is None
    num, go = 0, True
    while go:
        num += 1
        i, j = 0, 0
        while True:
            if j == max_y:
                cave[i, j] = "o"
                break
            elif empty(i, j + 1):
                j = j + 1
            elif empty(i - 1, j + 1):
                i, j = i - 1, j + 1
            elif empty(i + 1, j + 1):
                i, j = i + 1, j + 1
            else:
                cave[i, j] = "o"
                if i == 0 and j == 0:
                    go = False
                break
    return num
                
# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

cave = get_cave(get_rock_paths(file_name))
num = drop_sand_in_the_void(cave)
print_cave(cave)
print(f"Number of sand units: {num}")  # 665

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

cave = get_cave(get_rock_paths(file_name))
num = drop_sand_on_the_floor(cave)
#print_cave(cave)
print(f"Number of sand units: {num}")  # 25434
