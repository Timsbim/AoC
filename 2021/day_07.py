# Day 7
from pprint import pprint
from collections import Counter
from functools import lru_cache


# Reading input
with open("2021/input/day_07.csv", "r") as file:
    positions_input = [int(n) for n in file.read().strip().split(",")]
#positions_input = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
#print(positions)


# Part 1
print("Part 1:")

positions = Counter(positions_input)
"""
msg = "Fuel cost for aligning in position {}: {}"
for pos in range(min(positions), max(positions) + 1):
    cost = sum(
        abs(p - pos) * number
        for p, number in positions.items()
    )
    print(msg.format(pos, cost))
"""
min_cost = min(
    sum(abs(q - p) * number for q, number in positions.items())
    for p in range(min(positions), max(positions) + 1)
)
print(f"Minimal costs for aligning crabs: {min_cost}")


#Part 2
print("Part 2:")


@lru_cache(maxsize=None)
def fuel_costs(steps):
    if steps in {0, 1}:
        return steps
    return steps * (steps + 1) // 2

positions = Counter(positions_input)
"""
msg = "Fuel cost for aligning in position {}: {}"
for pos in range(min(positions), max(positions) + 1):
    cost = sum(
        fuel_costs(abs(p - pos)) * number
        for p, number in positions.items()
    )
    print(msg.format(pos, cost))
"""
min_cost = min(
    sum(fuel_costs(abs(q - p)) * number for q, number in positions.items())
    for p in range(min(positions), max(positions) + 1)
)
print(f"Minimal costs for aligning crabs: {min_cost}")
