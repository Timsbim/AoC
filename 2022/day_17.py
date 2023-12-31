# --------------------------------------------------------------------------- #
#    Day 17                                                                   #
# --------------------------------------------------------------------------- #

from itertools import cycle, islice
from textwrap import dedent

DAY = 17
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_jets(file_name):
    direction = {"<": -1, ">": 1}
    with open(file_name, "r") as file:
        jets = file.read().rstrip()
    for jet in cycle(jets):
        yield direction[jet]


def get_number_of_jets(file_name):
    with open(file_name, "r") as file:
        return len(file.read().rstrip())
        
# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

PIECES = [
    "..####",
    "...#\n..###\n...#\n",
    "....#\n....#\n..###",
    "..#\n..#\n..#\n..#",
    "..##\n..##"
]


def get_pieces():
    pieces = cycle(
        [{i for i, c in enumerate(row) if c == "#"}
          for row in reversed(dedent(block).splitlines())]
        for block in PIECES
    ) 
    yield from cycle(pieces)


def print_stack(stack):
    print(
        "+" + "-" * 7 + "+\n"
        + "\n".join(
            "|" + "".join("#" if n in row else "." for n in range(7)) + "|"
            for row in reversed(stack)
        ) + "\n+" + "-" * 7 + "+\n"
    )


def move(piece, jet, stack_rows):
    #stack_rows += [set() for _ in range(max(len(piece) - len(stack_rows), 0))]
    if jet == -1 and 0 < min(map(min, piece)):
        new_piece = [{n - 1 for n in row} for row in piece]        
    elif jet == 1 and max(map(max, piece)) < 6:
        new_piece = [{n + 1 for n in row} for row in piece]
    else:
        return piece
    if all(np.isdisjoint(s) for np, s in zip(new_piece, stack_rows)):
        return new_piece
    return piece


def can_fall(piece, next_stack_rows):
    return all(p.isdisjoint(nsr) for p, nsr in zip(piece, next_stack_rows))
    

def drop_piece(stack, piece, jets):
    # The first 4 drops in empty space
    for _, jet in zip(range(4), jets):
        piece = move(piece, jet, [])

    # Rest
    piece_height, stack_height = len(piece), len(stack)
    row = 0
    for j in range(stack_height - 1, -1, -1):
        next_stack_rows = stack[j:j + piece_height + 1]
        if not can_fall(piece, next_stack_rows):
            row = j + 1
            break
        piece = move(piece, next(jets), next_stack_rows)

    # Adjust stack accordingly
    num_new_rows = (row + piece_height) - stack_height
    for _ in range(num_new_rows):
        stack.append(set())
    for j in range(row, row + piece_height):
        stack[j].update(piece[j - row])
  
# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def drop_pieces(num, pieces, jets, stack=None):
    if stack is None:
        stack = []
    for piece in islice(pieces, num):
        drop_piece(stack, piece, jets)
    return stack


pieces, jets = get_pieces(), get_jets(file_name)
stack = drop_pieces(2022, pieces, jets)
print(len(stack))  # 3151

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="\n")


def detect_pattern(stack, cut_off=100_000):
    cut_off = cut_off
    part = stack[cut_off - 1:]
    pattern = []
    for j in range(cut_off, len(stack) - 1):
        part.pop()
        if part == stack[-len(part):]:
            pattern.append(j)
        if len(pattern) == 2:
            break
    else:
        return None, None
    period = pattern[1] - pattern[0]
    for i in range(len(stack) - 2 * period):
        if stack[i:i + period] == stack[i + period: i + 2 * period]:
            return i, period


def drop_lines(num_lines, pieces, jets, stack):
    num_lines += len(stack)
    go = True
    while go:
        for n, piece in enumerate(pieces, 1):
            drop_piece(stack, piece, jets)
            if len(stack) >= num_lines:
                go = False
                break
    return n


sample_height = 50_000
pieces, jets = get_pieces(), get_jets(file_name)
stack = drop_pieces(sample_height, pieces, jets)
start_height, period_height = detect_pattern(stack, 20_000)
print(f"Start height: {start_height} - Pattern height: {period_height}")

pieces, jets = get_pieces(), get_jets(file_name)
stack = []
num_start_pieces = drop_lines(start_height, pieces, jets, stack)
drop_lines(period_height, pieces, jets, stack)
num_period_pieces = drop_lines(period_height, pieces, jets, stack)
print(f"Start pieces: {num_start_pieces} - Pieces per period: {num_period_pieces}")

num_periods, num_rest_pieces = divmod(10**12 - num_start_pieces, num_period_pieces)
base_height = start_height + period_height * num_periods
print(f"Base height: {base_height}")

pieces, jets = get_pieces(), get_jets(file_name)
stack = drop_pieces(num_start_pieces + num_rest_pieces, pieces, jets)
rest_height = len(stack) - start_height
print(f"Final height: {base_height + rest_height}")  # 1560919540245
