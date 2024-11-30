# --------------------------------------------------------------------------- #
#    Day 9                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 9
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    histories = [list(map(int, line.split())) for line in file]
if EXAMPLE:
    pprint(histories)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

def both_parts(histories):
    solution_1 = solution_2 = 0
    for history in histories:
        row, starts, ends = history, [history[0]], [history[-1]]
        while any(n != 0 for n in row):
            row = [n - m for n, m in zip(row[1:], row)]
            starts.append(row[0])
            ends.append(row[-1])
        delta_1 = delta_2 = 0
        for start, end in reversed(list(zip(starts, ends))):
            delta_2, delta_1 = start - delta_2, end + delta_1
        solution_1 += delta_1
        solution_2 += delta_2
    return solution_1, solution_2


solution_1, solution_2 = both_parts(histories)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

if not EXAMPLE:
    assert solution_1 == 2005352194
print(solution_1)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

if not EXAMPLE:
    assert solution_2 == 1077
print(solution_2)
