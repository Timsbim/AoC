# Day 14
from pprint import pprint
import re
from collections import Counter


DAY = 14
EXAMPLE = True


# Preparation
file_name = f"2021/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"


# Reading input
with open(file_name, "r") as file:
    template_input = list(next(file).rstrip())
    next(file)
    insertions = {
        tuple(pair): insert
        for pair, insert in (
            line.strip().split(" -> ") for line in file
        )
    }
print("\nInput:")
print("Template:", template_input)
print("Insertions:")
pprint(insertions)

# Helper function


# Part 1
print("\nPart 1:")


def step(template, insertions):
    return [
        c
        for l, r in zip(template[:-1], template[1:])
        for c in [l, insertions[l, r]]
    ] + [template[-1]]


display = False
template = template_input[:]
if display:
    print("Template:", "".join(template))
for i in range(1, 10 + 1):
    template = step(template, insertions)
    if display:
        print(f"After step {i}:", "".join(template))
counts = set(Counter(template).values())
maximum, minimum = max(counts), min(counts)
print(
    f"Max-count minus min-count after {i} steps:",
    maximum - minimum
)


# Part 2
print("\nPart 2:")


def steps(template, insertions, nsteps):
    for _ in range(nsteps):
        template = step(template, insertions)
    return template


template = template_input[:]
base_insertions = {
    pair: steps(list(pair), insertions, 20) for pair in insertions
}
base_counts = {
    pair: Counter(base_insertions[pair]) for pair in insertions
}
# pprint(base_counts)

counts = Counter()
counts.subtract(Counter(template[1:-1]))
for pair in zip(template[:-1], template[1:]):
    t = base_insertions[pair]
    counts.subtract(Counter(t[1:-1]))
    for p in zip(t[:-1], t[1:]):
        counts.update(base_counts[p])
counts = set(counts.values())
maximum, minimum = max(counts), min(counts)
print(
    f"Max-count minus min-count after 40 steps:",
    maximum - minimum
)


template = template_input[:]
base_insertions = {
    pair: steps(list(pair), insertions, 20) for pair in insertions
}
base_counts = {
    pair: Counter(base_insertions[pair]) for pair in insertions
}

counts = Counter()
counts.subtract(Counter(template[1:-1]))
stack = [(pair, 1) for pair in zip(template[:-1], template[1:])]
while stack:
    pair, level = stack.pop()
    if level == 2:
        counts.update(base_counts[pair])
    else:
        template = base_insertions[pair]
        counts.subtract(Counter(template[1:-1]))
        stack.extend(
            (pair, level + 1)
            for pair in zip(template[:-1], template[1:])    
        )

counts = set(counts.values())
maximum, minimum = max(counts), min(counts)
print(
    f"Max-count minus min-count after 40 steps:",
    maximum - minimum
)
