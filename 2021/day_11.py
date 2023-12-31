# Day 11
from pprint import pprint
from collections import Counter


# Reading input
with open("2021/day_11_input.csv", "r") as file:
    levels_input = [
        [int(number) for number in line.strip()]
        for line in file
    ]
pprint(levels_input)


# Helper function

def adjacents(i, j, levels):
    return {
        pair for pair in product(
            range(max(0, i - 1), min(len(levels) - 1, i + 1) + 1),
            range(max(0, j - 1), min(len(levels[0]) - 1, j + 1) + 1),
        )
    } - {(i, j)}


# Part 1
print("Part 1:")

def step(levels):
    rows, cols = len(levels), len(levels[0])
    adjacent = Counter((i, j) for i in range(rows) for j in range(cols))
    flashing = set()
    while adjacent:
        new = set()
        for (i, j), n in adjacent.items():
            levels[i][j] += n
            if levels[i][j] > 9:
                new.add((i, j))
                levels[i][j] = 0
        flashing.update(new)
        adjacent = Counter(
            adj
            for point in new
            for adj in adjacents(*point, levels) - flashing
        )
    return len(flashing)


levels = [level[:] for level in levels_input]
steps = 200
num_flashes = 0
for n in range(1, steps + 1):
    num_flashes += step(levels)
    print(f"Step {n:>3}: # flashes = {num_flashes}")
    pprint(levels)


# Part 2
print("\nPart 2:")

levels = [level[:] for level in levels_input]
num_octopuses = len(levels) * len(levels[0])
s = 0
while True:
    s += 1
    if step(levels) == num_octopuses:
        break
print(f"First all-octopus-flash step: {s}")
