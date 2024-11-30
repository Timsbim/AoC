# --------------------------------------------------------------------------- #
#    Day 10                                                                   #
# --------------------------------------------------------------------------- #
from itertools import chain, product


DAY = 10
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
    maze = []
    for line in file:
        maze.append(list(line.strip()))
maze = list(reversed(maze))
if EXAMPLE:
    print("\nThe amazing MAZE:\n")
    with open(file_name, "r") as file:
        print(file.read(), end="\n\n")

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

def find_start(maze):
    height, width = len(maze), len(maze[0])
    for position in product(range(height), range(width)):
        y, x = position
        if maze[y][x] != "S":  # Nope
            continue
        if 0 < y and maze[y - 1][x] in {"|", "L", "J"}:  # down
            return position, (y - 1, x)
        if 0 < x and maze[y][x - 1] in {"-", "L", "F"}:  # left
            return position, (y, x - 1)
        if y < height - 1 and maze[y + 1][x] in {"|", "7", "F"}:  # up
            return position, (y + 1, x)
        if x < width - 1 and maze[y][x + 1] in {"-", "J", "7"}:  # right
            return position, (y, x + 1)


def next_step(position, next_position):
    (y0, x0), (y1, x1) = position, next_position
    dy, dx = y1 - y0, x1 - x0
    part = maze[y1][x1]
    if part == "|":  # Up or down
        return y1 + dy, x0
    if part == "-":  # Right or left
        return y0, x1 + dx
    if part == "L":  # Up and left or down and right
        return y0 + (-1 if dx == 0 else 1), x0 + (-1 if dy == 0 else 1)
    if part == "J":  # Up and right down and left
        return y0 + (-1 if dx == 0 else 1), x0 + (1 if dy == 0 else -1)
    if part == "7":  # Up and left down and right
        return y0 + (1 if dx == 0 else -1), x0 + (1 if dy == 0 else -1)
    if part == "F":  # Up and right or down and left
        return y0 + (1 if dx == 0 else -1), x0 + (-1 if dy == 0 else 1)


def search_loop(maze):
    pos_0, pos_1 = find_start(maze)
    start, loop = pos_0, [pos_0]
    while True:
        pos_0, pos_1 = pos_1, next_step(pos_0, pos_1)
        loop.append(pos_0)
        if pos_1 == start:
            return loop


# Just for fun
def print_loop(maze, loop):
    trans = {
        "|": "\u2503", "-": "\u2501",
        "L": "\u2517", "J": "\u251B",
        "7": "\u2513", "F": "\u250F",
        "S": " "
    }
    loop = {(y, x): trans[maze[y][x]] for y, x in loop}
    height, width = len(maze), len(maze[0])
    strings = [
        "".join(loop.get((y, x), " ") for x in range(width))
        for y in range(height)
    ]
    print("\n" + "\n".join(reversed(strings)))

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(loop):
    length = len(loop)
    return length // 2 if length % 2 == 0 else (length - 1) // 2


loop = search_loop(maze)
solution = part_1(loop)
if not EXAMPLE:
    assert solution == 6860
else:
    print("\n\nThe amazing LOOP:")
    print_loop(maze, loop)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(loop):

    # Resize the loop to account for the squeezing:
    # - Minimize the coverd area by shifting the loop as much as possible
    #   towards the origin (-> min_y and min_x as offset)
    # - Insert a new row/column between every consecutive rows/columns (ie.
    #   multiply loop coordinates by 2) and fill the gaps in the loop
    #   accordingly
    min_y = min_x = float("inf")
    max_y = max_x = float("-inf")
    for y, x in loop:
        min_y, max_y = min(y, min_y), max(y, max_y)
        min_x, max_x = min(x, min_x), max(x, max_x)
    loop = (((y - min_y) * 2, (x - min_x) * 2) for y, x in loop)
    y0, x0 = next(loop)
    new_loop = [(y0, x0)]
    for y1, x1 in chain(loop, [(y0, x0)]):
        new_loop.append((y0 + (y1 - y0) // 2, x0 + (x1 - x0) // 2))
        new_loop.append((y1, x1))
        y0, x0 = y1, x1
    loop = set(new_loop)
    
    height, width = 2 * (max_y - min_y) + 1, 2 * (max_x - min_x) + 1
    def neighbours(y, x):
        if 0 <= y:
            yield y - 1, x
        if y < height:
            yield y + 1, x
        if 0 <= x:
            yield y, x - 1
        if x < width:
            yield y, x + 1

    # BFS for reaching all points outside the area enclosed by the loop
    outer = {(-1, -1)} | loop
    edge = {(-1, -1)}
    while edge:
        next_edge = set()
        for y, x in edge:
            for position in neighbours(y, x):
                if position not in outer:
                    next_edge.add(position)
                    outer.add(position)
        edge = next_edge

    # Collect the original interior points by discarding the added rows
    # and columns (ie. those with an odd coordinate)
    size_inner = 0
    for y, x in product(range(height), range(width)):
        if (y, x) not in outer and y % 2 != 1 and x % 2 != 1:
            size_inner += 1
    return size_inner


solution = part_2(loop)
if not EXAMPLE:
    assert solution == 343
print(solution)
