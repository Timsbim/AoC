# Day 2
from collections import Counter


# Reading input
with open("2021/input/day_02.csv", "r") as file:
    steps = [
        (step, int(number))
        for step, number in (line.rstrip().split(" ") for line in file)
    ]
print(steps)


# Part 1
accounting = {"forward": 0, "down": 0, "up": 0}
for step, number in steps:
    accounting[step] += number
print(accounting)
print(accounting["forward"] * (accounting["down"] - accounting["up"]))

accounting = Counter(
    [move for step, number in steps for move in [step] * number]
)
print(accounting)
print(accounting["forward"] * (accounting["down"] - accounting["up"]))

accounting = sum(
    (Counter([step] * number) for step, number in steps), Counter([])
)
print(accounting)
print(accounting["forward"] * (accounting["down"] - accounting["up"]))


# Part 2
"""
steps = [
    ("forward", 5), ("down", 5), ("forward", 8), ("up", 3), ("down", 8),
    ("forward", 2)
]
"""
aim = horizontal = depth = 0
for step, number in steps:
    if step == "down":
        aim += number
    elif step == "up":
        aim -= number
    else:
        horizontal += number
        depth += (aim * number)
print(f"{aim = }, {horizontal = }, {depth = }")
print(f"{horizontal * depth = }")
