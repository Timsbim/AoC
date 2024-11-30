# Day 5
from pprint import pprint
from collections import Counter


# Reading input
with open("2021/input/day_05.csv", "r") as file:
    lines = [
        tuple(
            tuple(int(n) for n in pair.split(",")) for pair in line.split("->")
        )
        for line in file
    ]
#pprint(lines)


# Part 1
print("Part 1:")

counter = Counter()
for (x1, y1), (x2, y2) in lines:
    if x1 == x2 or y1 == y2:
        (x1, y1), (x2, y2) = sorted([(x1, y1), (x2, y2)])
        counter += Counter(
            (x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)
        )
hot_points = [item for item, count in counter.items() if count > 1]
count = len(hot_points)
print(f"{count = }")


#Part 2
print("Part 2:")

counter = Counter()
for (x1, y1), (x2, y2) in lines:
    if x1 == x2 or y1 == y2:
        (x1, y1), (x2, y2) = sorted([(x1, y1), (x2, y2)])
        counter += Counter(
            (x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)
        )
    elif x2 - x1 == y2 - y1 or x2 - x1 == y1 - y2:
        (x1, y1), (x2, y2) = sorted([(x1, y1), (x2, y2)])
        if y1 <= y2:
            y_range = range(y1, y2 + 1)
        else:
            y_range = range(y1, y2 - 1, -1)
        counter += Counter(zip(range(x1, x2 + 1), y_range))
hot_points = [item for item, count in counter.items() if count > 1]
count = len(hot_points)
print(f"{count = }")
