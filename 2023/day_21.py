# --------------------------------------------------------------------------- #
#    Day 21                                                                   #
# --------------------------------------------------------------------------- #
from itertools import product
from pprint import pprint


DAY = 21
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

with open(file_name, "r") as file:
    grid = file.read()
    if EXAMPLE:
        print(grid)
    GRID = tuple(map(tuple, grid.splitlines()))

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

HEIGHT, WIDTH = len(GRID), len(GRID[0])
STOP_Y, STOP_X = HEIGHT - 1, WIDTH - 1
START_Y, START_X = HEIGHT // 2, WIDTH // 2
PLOTS = {
    (y, x)
    for y, x in product(range(HEIGHT), range(WIDTH))
    if GRID[y][x] in (".", "S")
}

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def neighbours(y, x):
    for n in (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x):
        if n in PLOTS:
            yield n


def part_1(steps):
    y0, x0 = HEIGHT // 2, WIDTH // 2
    step, paths = 0, {(y0, x0)}
    while step < steps:
        next_paths = set()
        for y, x in paths:
            for n in neighbours(y, x):
                next_paths.add(n)
        paths = next_paths
        step += 1
        if step == steps:
            return len(paths)
    

solution = part_1(6 if EXAMPLE else 64)
assert solution == (16 if EXAMPLE else 3782)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def print_dists(distances, size):
    for y in range(-size - 1, HEIGHT + size + 1):
        line = []
        for x in range(-size - 1, WIDTH + size + 1):
            char = "  "
            if (dist := distances.get((y, x), -1)) >= 0:
                char = f"{dist: >2}"
            elif y % HEIGHT == 0 or x % WIDTH == 0:
                char =  " +"
            line.append(char)
        print("".join(line))


def neighbours(y, x):
    for y1, x1 in (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x):
        if (y1 % HEIGHT, x1 % WIDTH) in PLOTS:
            yield y1, x1


def walk(steps):
    y0, x0 = HEIGHT // 2, WIDTH // 2
    distances = {(y0, x0): 0}
    step, paths = 1, {(y0, x0)}
    while step <= steps:
        next_paths = set()
        for y, x in paths:
            for n in neighbours(y, x):
                if n not in distances:
                    distances[n] = step
                    next_paths.add(n)
        paths = next_paths
        step += 1
    return distances


def manhattan(y, x):
    return abs(y - START_Y) + abs(x - START_X)


def diffs(dists, r0, c0, r1, c1):
    inf = float("inf")
    quadrants = []
    for r, c in (r0, c0), (r1, c1):    
        y0, x0 = r * HEIGHT, c * WIDTH
        y1, x1 = y0 + HEIGHT, x0 + WIDTH
        quadrants.append(product(range(y0, y1), range(x0, x1)))
    return all(
        dists.get(p0, inf) == dists.get(p1, inf)
        for p0, p1 in zip(*quadrants)
    )


def find_max_grid(pattern):
    min_y = min_x = 0
    max_y = max_x = float("-inf")
    for y, x in pattern:
        min_y, min_x = min(min_y, y), min(min_x, x)
        max_y, max_x = max(max_y, y), max(max_x, x)
    
    limits = {}
    c = 0
    while True:
        if max_y < (c + 1) * HEIGHT:
            return None
        if diffs(pattern, 0, c, 0, c + 1):
            limits[0, 1] = c
            break
        c += 1
    r = 0
    while True:
        if max_x < (r + 1) * WIDTH:
            return None
        if diffs(pattern, r, 0, r + 1, 0):
            limits[1, 0] = r
            break
        r += 1
    c = 0
    while True:
        if (c - 1) * HEIGHT < min_y:
            return None
        if diffs(pattern, 0, c, 0, c - 1):
            limits[0, -1] = abs(c)
            break
        c -= 1
    r = 0
    while True:
        if (r - 1) * WIDTH < min_x:
            return None
        if diffs(pattern, r, 0, r - 1, 0):
            limits[-1, 0] = abs(r)
            break
        r -= 1

    return max(limits.values())


def tiles(r, c):
    y0, x0 = r * HEIGHT, c * WIDTH
    yield from product(range(y0, y0 + HEIGHT), range(x0, x0 + WIDTH))


def part_2(steps):
    inf = float("inf")
    
    distances = walk(10 * max(HEIGHT, WIDTH))
    pattern = {
        (y, x): dist - manhattan(y, x)
        for (y, x), dist in distances.items()
    }
    n = find_max_grid(pattern)
    if n is None:
        print("Coundn't find patterns, something went wrong!")
        return
    TOP, BOTTOM = -n * HEIGHT, (n + 1) * HEIGHT
    LEFT, RIGHT = -n * WIDTH, (n + 1) * WIDTH

    def distance(y, x, default=inf):
        dist = manhattan(y, x)
        if  y < TOP:
            y = TOP + y % HEIGHT
        elif BOTTOM <= y:
            y = BOTTOM - (HEIGHT - y % HEIGHT)
        if x < LEFT:
            x = LEFT + x % WIDTH
        elif RIGHT <= x:
            x = RIGHT - (WIDTH - x % WIDTH)
        
        return dist + pattern.get((y, x), default)

    SYNC = steps % 2
    
    def count_tile(r, c):
        return sum(
            1
            for y, x in tiles(r, c)
            if manhattan(y, x) % 2 == SYNC and distance(y, x) <= steps
        )

    full_count = {1: count_tile(0, 0), 0: count_tile(1, 0)}

    # The following can be simplified (I didn't have the nerve)
    r0 = (HEIGHT // 2 + steps) // HEIGHT + 1
    c0 = (WIDTH // 2 + steps) // WIDTH + 1
    count = full_count[1]
    for r in range(-r0, 0):
        count += count_tile(r, 0)
        if all(distance(y, x, 0) <= steps for y, x in tiles(r, 0)):
            for r in range(r + 1, 0):
                count += full_count[(r + 1) % 2]
            break
    for r in range(r0, 0, -1):
        count += count_tile(r, 0)
        if all(distance(y, x, 0) <= steps for y, x in tiles(r, 0)):
            for r in range(r - 1, 0, -1):
                count += full_count[(r + 1) % 2]
            break
    for c in range(-c0, 0):
        count += count_tile(0, c)
        if all(distance(y, x, 0) <= steps for y, x in tiles(0, c)):
            for c in range(c + 1, 0):
                count += full_count[(c + 1) % 2]
            break
    for c in range(c0, 0, -1):
        count += count_tile(0, c)
        if all(distance(y, x, 0) <= steps for y, x in tiles(0, c)):
            for c in range(c - 1, 0, -1):
                count += full_count[(c + 1) % 2]
            break        
    for c in range(-c0 + 1, 0):
        count += count_tile(1, c) * -c
        if all(distance(y, x, 0) <= steps for y, x in tiles(1, c)):
            for c in range(c + 1, 0):
                count += full_count[c % 2] * -c
            break
    for c in range(c0 - 1, 0, -1):
        count += count_tile(1, c) * c
        if all(distance(y, x, 0) <= steps for y, x in tiles(1, c)):
            for c in range(c - 1, 0, -1):
                count += full_count[c % 2] * c
            break
    for c in range(-c0 + 1, 0):
        count += count_tile(-1, c) * -c
        if all(distance(y, x, 0) <= steps for y, x in tiles(-1, c)):
            for c in range(c + 1, 0):
                count += full_count[c % 2] * -c
            break
    for c in range(c0 - 1, 0, -1):
        count += count_tile(-1, c) * c
        if all(distance(y, x, 0) <= steps for y, x in tiles(-1, c)):
            for c in range(c - 1, 0, -1):
                count += full_count[c % 2] * c
            break
    
    return count

    
solution = part_2(5_000 if EXAMPLE else 26_501_365)
assert solution == (16733044 if EXAMPLE else 630661863455116)
print(solution)
