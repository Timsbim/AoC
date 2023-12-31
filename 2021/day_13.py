# Day 13
from pprint import pprint
import re
from itertools import zip_longest


# Preparation
DAY = 13
EXAMPLE = False
file_name = f"2021/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"


# Reading input
re_fold = re.compile(r"^.*?(x|y)=(\d+)$")
coordinates_input = []
folding_input = []
with open(file_name, "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        if line.startswith("fold"):
            axis, position = re_fold.match(line).groups()
            folding_input.append((axis, int(position)))
        else:
            coordinates_input.append(tuple(int(n) for n in line.split(",")))
coordinates_input = [(y, x) for x, y in coordinates_input]
rows = max(x for x, _ in coordinates_input) + 1
cols = max(y for _, y in coordinates_input) + 1
paper_input = [[" "] * cols for _ in range(rows)]
for x, y in coordinates_input:
    paper_input[x][y] = "*"
# pprint(coordinates_input)
# pprint(folding_input)
# pprint(paper_input)


# Helper function
def print_paper(paper, lmargin=4, vmargin=2):
    lmargin = " " * lmargin
    vmargin = [" " * len(paper[0])] * vmargin
    print(
        "\n".join(
            lmargin + "".join(line)
            for line in vmargin + paper + vmargin
        )
    )

# print_paper(paper_input)


# Part 1
print("Part 1:")

paper = paper_input[:]
rows, cols = len(paper), len(paper[0])
print(f"{rows = }, {cols = }")

def fold_paper(paper, axis, position):
    
    # Copy input data
    paper = [line[:] for line in paper]

    # Flip, if folding along column
    if axis == "x":
        paper = [list(line) for line in zip(*paper)]

    # Fold
    paper = [
        [
            "*" if "*" in {c_1, c_2} else " "
            for c_1, c_2 in zip(line_1, line_2)
        ]
        for line_1, line_2 in zip_longest(
            paper[position - 1::-1],
            paper[position + 1:],
            fillvalue=tuple(" " for _ in range(len(paper[0])))
        )    
    ][::-1]
      
    # Flip back, if folding along column
    if axis == "x":
        paper = [list(line) for line in zip(*paper)]

    return paper


display = False
if display:
    print_paper(paper)
for i in range(2):
    paper = fold_paper(paper, *folding_input[i])
    if i == 0:
        num_points = sum(line.count("*") for line in paper)
        print(f"Points after first folding: {num_points}")
    if display:
        print_paper(paper)


# Part 2
print("\nPart 2:")

paper = paper_input[:]
for axis, position in folding_input:
    paper = fold_paper(paper, axis, position)
print_paper(paper)
