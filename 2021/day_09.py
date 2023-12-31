# Day 9
from pprint import pprint
from operator import itemgetter
from heapq import nlargest
from math import prod


# Reading input
with open("2021/day_09_input.csv", "r") as file:
    numbers = [[int(number) for number in line.strip()] for line in file]
"""
numbers = [
    [int(number) for number in line]
    for line in [
        "2199943210", "3987894921", "9856789892", "8767896789", "9899965678"
    ]
]
"""
# pprint(numbers)


# Part 1
print("Part 1:")


def adjacents(i, j, numbers):
    return (
        {(i, k) for k in range(max(0, j - 1), min(len(numbers[0]) - 1, j + 1) + 1)}
        | {(k, j) for k in range(max(0, i - 1), min(len(numbers) - 1, i + 1) + 1)}
    ) - {(i, j)}


def is_lowpoint(i, j, numbers):
    return all(numbers[k][l] > number for k, l in adjacents(i, j, numbers))


"""
i, j = 2, 2
print(f"{i = } - {j = } - number = {numbers[i][j]}")
for k, l in sorted(adjacents(i, j, n_rows, n_cols)):
    print(f"row {k} - col {l} - number: {numbers[k][l]}")
"""

n_rows, n_cols = len(numbers), len(numbers[0])
print(f"{n_rows = }, {n_cols = }")
lows = []
no = 0
print("Lowpints:")
for i, row in enumerate(numbers):
    for j, number in enumerate(row):
        if is_lowpoint(i, j, numbers):
            lows.append((i, j, number + 1))
            no += 1
            # print(f"({no:->3}) row {i:>2} - column {j:>2} - {number = }")

# print(lows)
sum_of_lows = sum(n[2] for n in lows)
print(f"Sum of risk levels of low points: {sum_of_lows}")
coordinates = itemgetter(0, 1)
low_points = {coordinates(n) for n in lows}
# pprint(low_points)


# Part 2
print("Part 2:")


def built_basin(i, j, numbers):
    basin = set()
    stack = [(i, j)]
    while stack:
        point = stack.pop()
        basin.add(point)
        stack.extend(
            (k, l)
            for k, l in adjacents(*point, numbers) - basin
            if numbers[k][l] < 9
        )
    return basin


basin_sizes = [len(built_basin(*point, numbers)) for point in low_points]
result = prod(nlargest(3, basin_sizes))
print(f"Product of the 3 largest basin sizes: {result}")
