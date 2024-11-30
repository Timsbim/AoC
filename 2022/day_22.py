# --------------------------------------------------------------------------- #
#    Day 22                                                                   #
# --------------------------------------------------------------------------- #

import re
from itertools import product

DAY = 22
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

def get_map_and_path(file_name):
    with open(file_name, "r") as file:
        strings = file.read().splitlines()   
    board = strings[:-2]
    width = max(len(row) for row in board)
    board = [list(row.ljust(width)) for row in board]
    path = re.findall(r"\d+|[A-Z]", strings[-1])
    path = [int(p) if p.isdigit() else p for p in path]
    return board, path

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

DIRS = {
    "R": (0, 1), "U": (-1, 0), "L": (0, -1), "D": (1, 0),
    (0, 1): "R", (-1, 0): "U", (0, -1): "L", (1, 0): "D"
}


def print_board(board):
    print("\n".join(map("".join, board)))


def limits(sequence, pos):
    start = 0
    for i in range(pos - 1, -1, -1):
        if sequence[i] == " ":
            start = i + 1
            break
    stop = len(sequence) - 1
    for i in range(pos + 1, len(sequence)):
        if sequence[i] == " ":
            stop = i - 1
            break
    return start, stop


def one_step(sequence, pos):
    start, stop = limits(sequence, pos)
    if start == stop:
        return pos
    left = right = pos
    if start < pos < stop:
        if sequence[pos - 1] != "#":
            left = pos - 1
        if sequence[pos + 1] != "#":
            right = pos + 1
    elif start == pos:
        if sequence[stop] != "#":
            left = stop
        if sequence[pos + 1] != "#":
            right = pos + 1
    elif pos == stop:
        if sequence[pos - 1] != "#":
            left = pos - 1
        if sequence[start] != "#":
            right = start
    return left, right


def build_graph(board):
    width, height = len(board[0]), len(board)
    graph = {}
    for y, x in product(range(height), range(width)):
        if board[y][x] != ".":
            continue
        node = graph[y, x] = {"R": (y, x), "U": (y, x), "L": (y, x), "D": (y, x)}
        
        # Moving horizontally
        row = board[y]
        left, right = one_step(row, x)
        node["L"], node["R"] = (y, left), (y, right)

        # Moving vertically
        column = [board[j][x] for j in range(height)]
        up, down = one_step(column, y)
        node["U"], node["D"] = (up, x), (down, x)
    
    return graph


def turn(direction, instruction):
    y, x = direction
    if instruction == "R":
        return x, -y
    return -x, y


def move(graph, position, direction, steps, transitions=None):
    if transitions is None:
        transitions = set()
    direction = DIRS[direction]
    for _ in range(steps):
        next_position = position
        if (position, direction) in transitions:
            pos_position, pos_direction = transitions[position, direction]
            if pos_position in graph:
                next_position, direction = pos_position, pos_direction
        else:
            next_position = graph[position][direction]
        if position == next_position:
            break
        position = next_position
    return position, DIRS[direction]


def traverse(graph, start, path, transitions=None):
    direction = DIRS["R"]
    position = start
    print(position, "R")
    for instruction in path:
        if type(instruction) == str:
            direction = turn(direction, instruction)
        else:
            position, direction = move(
                graph, position, direction, instruction, transitions
            )
    row, column = position
    return row + 1, column + 1, DIRS[direction]


def score(row, column, facing):
    SCORES = {"R": 0, "D": 1, "L": 2, "U": 3}
    return 1_000 * row + 4 * column + SCORES[facing]

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="\n")

board, path = get_map_and_path(file_name)
start = 0, board[0].index(".")
graph = build_graph(board)
row, column, facing = traverse(graph, start, path)
print(score(row, column, facing))  # 1428

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def get_faces(board, size):
    width, height = len(board[0]), len(board)
    faces = {}
    no = 0
    for y, x in product(range(0, height, size), range(0, width, size)):
        if all(
            board[j][i] != " "
            for i, j in product(range(x, x + size), range(y, y + size))
        ):
            no += 1
            faces[no] = y, x
    return faces


def print_faces(faces, size=50, unit=10):
    size //= unit
    faces = {
        n: tuple(edge // unit for edge in face)
        for n, face in faces.items()
    }
    width, height = 0, 0
    for y, x in faces.values():
        if y > height:
            height = y
        if x > width:
            width = x
    width, height = width + size, height + size
    board = [[" "] * width for _ in range(height)]
    for n, (y, x) in faces.items():
        n = str(n)
        for j, i in product(range(y, y + size), range(x, x + size)):
            board[j][i] = n
    print("\n" + "\n".join("".join(row) for row in board))
    
    
size = 4 if EXAMPLE else 50
transitions = {}
if EXAMPLE:
    # 1
    transitions[1, 6] = {
        ((j, 3 * size - 1), "R"): ((3 * size - 1 - j, 4 * size - 1), "L")
        for j in range(size)
    }
    transitions[6, 1] = {
        ((j2, i2), "R"): ((j1, i1), "L")
        for ((j1, i1), _), ((j2, i2), _) in transitions[1, 6].items()
    }
    # 2
    transitions[1, 2] = {
        ((0, i), "U"):  ((size, 3 * size - 1 - i), "D")
        for i in range(2 * size, 3 * size)
    }
    transitions[2, 1] = {
        ((j2, i2), "U"): ((j1, i1), "D")
        for ((j1, i1), _), ((j2, i2), _) in transitions[1, 2].items()
    }
    # 3
    transitions[1, 3] = {
        ((j, 2 * size), "L"): ((size, j + size), "D")
        for j in range(size)
    }
    transitions[3, 1] = {
        ((j2, i2), "U"): ((j1, i1), "R")
        for ((j1, i1), _), ((j2, i2), _) in transitions[1, 3].items()
    }
    # 4
    transitions[2, 6] = {
        ((j, 0), "L"): ((3 * size - 1, 5 * size - 1 - j), "U")
        for j in range(size, 2 * size)
    }
    transitions[6, 2] = {
        ((j2, i2), "D"): ((j1, i1), "R")
        for ((j1, i1), _), ((j2, i2), _) in transitions[2, 6].items()
    }
    #5
    transitions[2, 5] = {
        ((2 * size - 1, i), "D"): ((3 * size - 1, 3 * size - 1 - i), "U")
        for i in range(size)
    }
    transitions[5, 2] = {
        ((j2, i2), "D"): ((j1, i1), "U")
        for ((j1, i1), _), ((j2, i2), _) in transitions[2, 5].items()         
    }
    # 6
    transitions[3, 5] = {
        ((2 * size - 1, i), "D"): ((4 * size - 1 - i, 2 * size), "R")
        for i in range(size, 2 * size)
    }
    transitions[5, 3] = {
        ((j2, i2), "L"): ((j1, i1), "U")
        for ((j1, i1), _), ((j2, i2), _) in transitions[3, 5].items()
    }
    # 7
    transitions[4, 6] = {
        ((j, 3 * size - 1), "R"): ((2 * size, 5 * size - 1 - j), "D")
        for j in range(size, 2 * size)
    }
    transitions[6, 4] = {
        ((j2, i2), "U"): ((j1, i1), "L")
        for ((j1, i1), _), ((j2, i2), _) in transitions[4, 6].items()
    }
else:
    # 1
    transitions[1, 6] = {
        ((0, i), "U"):  ((i + 2 * size, 0), "R") for i in range(size, 2 * size)
    }
    transitions[6, 1] = {
        ((j2, i2), "L"): ((j1, i1), "D")
        for ((j1, i1), _), ((j2, i2), _) in transitions[1, 6].items()        
    }
    # 2
    transitions[1, 4] = {
        ((j, size), "L"): ((3 * size - 1 - j, 0), "R") for j in range(size)
    }
    transitions[4, 1] = {
        ((j2, i2), "L"): ((j1, i1), "R")
        for ((j1, i1), _), ((j2, i2), _) in transitions[1, 4].items()
    }
    # 3
    transitions[2, 5] = {
        ((j, 3 * size - 1), "R"): ((3 * size - 1 - j, 2 * size - 1), "L")
        for j in range(size)
    }
    transitions[5, 2] = {
        ((j2, i2), "R"): ((j1, i1), "L")
        for ((j1, i1), _), ((j2, i2), _) in transitions[2, 5].items()
    }
    # 4
    transitions[2, 6] = {
        ((0, i), "U"): ((4 * size - 1, i - 2 * size), "U")
        for i in range(2 * size, 3 * size)
    }
    transitions[6, 2] = {
        ((j2, i2), "D"): ((j1, i1), "D")
        for ((j1, i1), _), ((j2, i2), _) in transitions[2, 6].items()
    }
    # 5
    transitions[2, 3] = {
        ((size - 1, i), "D"): ((i - size, 2 * size - 1), "L")
        for i in range(2 * size, 3 * size)
    }
    transitions[3, 2] = {
        ((j2, i2), "R"): ((j1, i1), "U")
        for ((j1, i1), _), ((j2, i2), _) in transitions[2, 3].items()
    }
    # 6
    transitions[3, 4] = {
        ((j, size), "L"): ((2 * size, j - size), "D") for j in range(size, 2 * size)
    }
    transitions[4, 3] = {
        ((j2, i2), "U"): ((j1, i1), "R")
        for ((j1, i1), _), ((j2, i2), _) in transitions[3, 4].items()
    }
    # 7
    transitions[5, 6] = {
        ((3 * size - 1, i), "D"): ((2 * size + i, size - 1), "L")
        for i in range(size, 2 * size)
    }
    transitions[6, 5] = {
        ((j2, i2), "R"): ((j1, i1), "U")
        for ((j1, i1), _), ((j2, i2), _) in transitions[5, 6].items()
    }

board, path = get_map_and_path(file_name)
graph = build_graph(board)
transitions = dict(
    transition
    for trans_dict in transitions.values()
    for transition in trans_dict.items()
    if transition[0][0] in graph
)
start = 0, board[0].index(".")
row, column, facing = traverse(graph, start, path, transitions)
print(score(row, column, facing))  # 142380
