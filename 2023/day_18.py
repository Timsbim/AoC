# --------------------------------------------------------------------------- #
#    Day 18                                                                   #
# --------------------------------------------------------------------------- #
from itertools import groupby, pairwise, product
from pprint import pprint


DAY = 18
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

TO_DIR = {"0": "R", "1": "D", "2": "L", "3": "U"}


def to_instruction(string):
    string = string.strip("()#")
    return TO_DIR[string[-1]], int(string[:-1], 16)


with open(file_name, "r") as file:
    dig_plan = []
    for line in file:
        dir_0, count_0, hex_string = line.rstrip().split()
        dir_1, count_1 = to_instruction(hex_string)
        dig_plan.append((dir_0, int(count_0), dir_1, count_1))

if EXAMPLE:
    pprint(dig_plan)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def looping(instructions):
    loop = [(0, 0)]
    for direction, count in instructions:
        y, x = loop[-1]
        if direction == "R":
            steps = ((y, x + i) for i in range(1, count + 1))
        elif direction == "D":
            steps = ((y + i, x) for i in range(1, count + 1))
        elif direction == "L":
            steps = ((y, x - i) for i in range(1, count + 1))
        else:  # direction == "U"
            steps = ((y - i, x) for i in range(1, count + 1))
        loop.extend(steps)
        
    return loop[:-1]


def fill_loop(loop):
    loop_set, loop_position = set(), {}
    min_y = min_x = float("inf")
    max_y = max_x = float("-inf")
    for n, (y, x) in enumerate(loop):
        loop_set.add((y, x))
        loop_position[y, x] = n
        min_y, max_y = min(y, min_y), max(y, max_y)
        min_x, max_x = min(x, min_x), max(x, max_x)

    length = len(loop)
    count = 0
    for y in range(min_y, max_y + 1):
        key = lambda x: (y, x) in loop_set
        segments = []
        for take, segment in groupby(range(min_x, max_x + 1), key=key):
            if take:
                segment = tuple(segment)
                segments.append((segment[0], segment[-1]))
        inner = False
        for x0, x1 in segments:
            if inner:
                count += x0 - last_x1 - 1
            n0, n1 = loop_position[y, x0], loop_position[y, x1]
            if n0 > n1:
                n0, n1 = n1, n0
            if x0 == x1 or loop[n0-1 % length][0] != loop[n1+1 % length][0]:
                inner = not inner
            last_x1 = x1

    return count + len(loop)


def part_1(dig_plan):
    instructions = ((direction, count) for direction, count, *_ in dig_plan)
    return fill_loop(looping(instructions))


solution = part_1(dig_plan)
assert solution == (62 if EXAMPLE else 49061)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def looping(instructions):
    loop, cols, rows = [(0, 0)], {0}, {0}
    for direction, count in instructions:
        y0, x0 = loop[-1]
        if direction == "R":
            y1, x1 = y0, x0 + count
        elif direction == "D":
            y1, x1 = y0 + count, x0
        elif direction == "L":
            y1, x1 = y0, x0 - count
        else:  # direction == "U"
            y1, x1 = y0 - count, x0
        loop.append((y1, x1))
        cols.add(y1)
        rows.add(x1)

    # Build a slightly larger loop by filling in missing grid parts.
    # Grid: defined by the loop points.
    cols, rows = sorted(cols), sorted(rows)
    grid = {
        (y, x): (n, m)
        for (n, y), (m, x) in product(enumerate(cols), enumerate(rows))
    }
    new_loop = []
    for (y0, x0), (y1, x1) in pairwise(loop):
        (n0, m0), (n1, m1) = grid[y0, x0], grid[y1, x1]
        if n0 == n1:
            ms = range(m0, m1) if m0 < m1 else range(m0, m1, -1)
            col = cols[n1]
            new_loop.extend((col, rows[m]) for m in ms)
        else:
            ns = range(n0, n1) if n0 < n1 else range(n0, n1, -1)
            row = rows[m1]
            new_loop.extend((cols[n], row) for n in ns)
    
    return new_loop


def fill_loop(loop):
    loop_set, loop_position, rows, cols = set(), {}, set(), set()
    for n, (y, x) in enumerate(loop):
        loop_set.add((y, x))
        loop_position[y, x] = n
        cols.add(y)
        rows.add(x)
    cols, rows = sorted(cols), sorted(rows)
    length = len(loop)
    last = length - 1

    def connected(y0, x0, y1, x1):
        abs_diff = abs(loop_position[y0, x0] - loop_position[y1, x1])
        return abs_diff == 1 or abs_diff == last

    count = 0
    for n, y in enumerate(cols):
        key = lambda x: (y, x) in loop_set
        segments = []
        for take, segment in groupby(rows, key=key):
            if take:
                segment = tuple(segment)
                if len(segment) == 1:
                    segments.append(segment * 2)
                else:
                    x0 = x1 = segment[0]
                    for x in segment[1:]:
                        if connected(y, x1, y, x):
                            x1 = x
                        else:
                            segments.append((x0, x1))
                            x0 = x1 = x
                    segments.append((x0, x1))        
        
        inner = False
        for x0, x1 in segments:
            if inner:
                count += x0 - last_x1 - 1
            n0, n1 = loop_position[y, x0], loop_position[y, x1]
            if n0 > n1:
                n0, n1 = n1, n0
            if x0 == x1 or loop[n0-1 % length][0] != loop[n1+1 % length][0]:
                inner = not inner
            last_x1 = x1

        xs = {x for segment in segments for x in segment}
        if n > 0:
            count_between = 0
            y0, y1 = cols[n-1], y
            inner = False
            cons = (x for x in xs & last_xs if connected(y0, x, y1, x))
            for x in sorted(cons):
                if inner:
                    count_between += x - last_x - 1
                inner = not inner
                last_x = x
            count += count_between * (y1 - y0 - 1)
        last_xs = xs

    return count + sum(
        abs(x1 - x0) if y1 == y0 else abs(y1 - y0)
        for (y0, x0), (y1, x1) in zip(loop, loop[1:] + [(0, 0)])
    )


def part_2(dig_plan):
    instructions = ((direction, count) for *_, direction, count in dig_plan)
    return fill_loop(looping(instructions))


solution = part_2(dig_plan)
assert solution == (952408144115 if EXAMPLE else 92556825427032)
print(solution)
