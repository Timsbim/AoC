# Day 20
from pprint import pprint
from itertools import permutations, product

DAY = 20
EXAMPLE = False


# Preparation
file_name = f"2021/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"


# Helper functions

def binit(string):
    return string.replace(".", "0").replace("#", "1")


def debinit(image):
    return [
        line.replace("0", ".").replace("1", "#") for line in image
    ]


def add_frame(image, pad):
    padding = pad
    if not all(line[0] == pad for line in image):
        padding += pad
    image = [padding + line for line in image]
    padding = pad    
    if not all(line[-1] == pad for line in image):
        padding += pad
    image = [line + padding for line in image]    
    padding = pad * len(image[0])
    num_lines = 2    
    if not all(c == pad for c in image[0]):
        num_lines += 1    
    image = [padding for _ in range(num_lines)] + image
    padding = pad * len(image[-1])
    num_lines = 2    
    if not all(c == pad for c in image[-1]):
        num_lines += 1    
    image =  image + [padding for _ in range(num_lines)]
    return image


def algo_position(image, i, j):
    start_col, end_col = j - 1, j + 2
    return int(
        "0b"
        + image[i-1][start_col:end_col]
        + image[i][start_col:end_col]
        + image[i+1][start_col:end_col],
        2
    )


def process(image, algorithm, steps):
    pad = "0"
    for _ in range(steps):
        image = add_frame(image, pad)
        image = [
            "".join(
                algorithm[algo_position(image, i, j)]
                for j in range(1, len(image[i]) - 1)
            )
            for i in range(1, len(image) - 1)
        ]
        pad = algorithm[int("0b" + pad * 9, 2)]
    return image


# Reading input
with open(file_name, "r") as file:
    algorithm = binit(next(file).strip())
    next(file)
    image_input = [binit(line.rstrip()) for line in file]


# Part 1
print("\nPart 1:")

image = image_input[:]
image = process(image, algorithm, 2)
print(sum(line.count("1") for line in image))
# 5786


# Part 2
print("\nPart 2:")

image = image_input[:]
image = process(image, algorithm, 50)
print(sum(line.count("1") for line in image))
# 16757
