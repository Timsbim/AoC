# Day 10
from pprint import pprint


# Reading input
with open("2021/input/day_10.csv", "r") as file:
    chunks = [line.strip() for line in file]
# pprint(chunks)


# Part 1
print("Part 1:")

pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
points = {")": 3, "]": 57, "}": 1197, ">": 25137}


def corruption_score(line):
    openings = []
    for c in line:
        if c in pairs:
            openings.append(c)
        else:
            if not openings or c != pairs[openings.pop()]:
                return points[c]
    return 0


scores = [corruption_score(line) for line in chunks]
# pprint(scores)
print(f"Total points: {sum(scores)}")


# Part 2
print("Part 2:")

points = {")": 1, "]": 2, "}": 3, ">": 4}


def completion_score(line):
    openings = []
    for c in line:
        if c in pairs:
            openings.append(c)
        else:
            if not openings or c != pairs[openings.pop()]:
                return 0
    closings = [pairs[opening] for opening in reversed(openings)]
    score = 0
    for closing in closings:
        score = score * 5 + points[closing]
    return score


scores = [
    score for score in (completion_score(line) for line in chunks) if score
]
middle_score = sorted(scores)[len(scores) // 2]
# print(scores)
print(f"Middle score: {middle_score}")
