# --------------------------------------------------------------------------- #
#    Day 8                                                                    #
# --------------------------------------------------------------------------- #

from math import prod

DAY = 8
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    numbers = [list(map(int, line.rstrip())) for line in file]

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

columns = [list(col) for col in zip(*numbers)]
visibles = 2 * (len(numbers) + len(numbers[0])) - 4
for i, row in enumerate(numbers[1:-1], 1):
    for j, n in enumerate(row[1:-1], 1):
        col = columns[j]
        sightlines = row[:j], row[j + 1:], col[:i], col[i + 1:]
        visibles += any(all(m < n for m in line) for line in sightlines)
print(visibles)  # 1647

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

def visibles(n, numbers):
    num = 0
    for m in numbers:
        num += 1
        if m >= n:
            break
    return num

scores = []
for i, row in enumerate(numbers[1:-1], 1):
    for j, n in enumerate(row[1:-1], 1):
        col = columns[j]
        sightlines = col[i - 1::-1], row[j - 1::-1], row[j + 1:], col[i + 1:]
        scores.append(prod(visibles(n, line) for line in sightlines))

print(max(scores))  # 392080
