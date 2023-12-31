# --------------------------------------------------------------------------- #
#    Day 25                                                                   #
# --------------------------------------------------------------------------- #

from pprint import pprint

DAY = 25
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2021/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    """
    translation = str.maketrans({".": "0", ">": "1", "v": "2"})
    positions = [
        line.rstrip().translate(translation) for line in file
    ]
    """
    #positions = file.read().split("\n")
    positions = [list(line.rstrip()) for line in file]

# pprint(positions)

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def steps(positions):
    rows, cols = len(positions), len(positions[0])
    row_index = list(range(cols))
    row_shift = row_index[1:] + [0]
    col_index = list(range(rows))
    col_shift = col_index[1:] + [0]
    steps = 0
    while True:
        stable = True
        steps += 1
        new_positions = []
        for row in positions:
            new_row = row[:]
            for i, j in zip(row_index, row_shift):
                if row[i] == ">" and row[j] == ".":
                    new_row[i] = "."
                    new_row[j] = ">"
                    stable = False
            new_positions.append(new_row)
        positions = new_positions
        new_positions = [
            position[:] for position in positions
        ]
        for i, j in zip(col_index, col_shift):
            for k, (current, after) in enumerate(
                zip(positions[i], positions[j])
            ):
                if current == "v" and after == ".":
                    new_positions[i][k] = "."
                    new_positions[j][k] = "v"
                    stable = False
        positions = new_positions
        if stable:
            break
    return steps

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

print(steps(positions))  # 579


# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

