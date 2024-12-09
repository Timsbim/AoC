# --------------------------------------------------------------------------- #
#    Day 18                                                                   #
# --------------------------------------------------------------------------- #
DAY = 18
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

if EXAMPLE:
    START, ROWS = ".^^.^.^^^^", 10
    print(f"Starting row:\n{START}")
else:
    with open("2016/input/day_18.txt", "r") as file:
        START = file.read().rstrip()
    ROWS = 40
COLS = len(START)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

TRAP = {"^^.", ".^^", "^..", "..^"}


def step(row):
    row = f".{row}."
    return "".join(
        "^" if row[i-1:i+2] in TRAP else "." for i in range(1, len(row) - 1)
    )


def solve(rows=ROWS):
    safe, row = START.count("."), START
    for _ in range(rows - 1):
        row = step(row)
        safe += row.count(".")
    return safe


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

print(solution := solve())
assert solution == (38 if EXAMPLE else 1961)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

print(solution := solve(rows=400_000))
assert solution == (1935478 if EXAMPLE else 20000795)
