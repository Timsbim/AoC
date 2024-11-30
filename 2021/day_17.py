# Day 17
from pprint import pprint
from math import ceil, sqrt
from operator import itemgetter

DAY = 17
EXAMPLE = False


# Preparation
file_name = f"2021/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"


# Reading input
with open(file_name, "r") as file:
    msg = file.read().strip()


# Helper functions

def step(x, y, v_x, v_y):
    return x + v_x, y + v_y, max(0, v_x - 1), v_y - 1


def steps(x, y, v_x, v_y, n):
    if n > 0:
        for s in range(1, n + 1):
            x, y, v_x, v_y = step(x, y, v_x, v_y)
            print(f"Step {s}:", x, y, v_x, v_y)
    return x, y, v_x, v_y

steps(0, 0, 6, 3, 9)


# Part 1
print("\nPart 1:")

x_min, x_max = 57, 116
y_min, y_max = -198, -148
target_area = (x_min, x_max, y_min, y_max)


def check(target_area):
    x_min, x_max, y_min, y_max = target_area

    # Determine minimal horizontal start velocity (v_x_start)
    v_x_min = ceil(sqrt(2 * x_min + 0.25) - 0.5)

    results = []
    for v_x_start in range(v_x_min, x_max // 2 + 1):
        for v_y_start in range(1, 3000):
            match = False
            x, y, v_x, v_y = 0, 0, v_x_start, v_y_start
            max_y = 0
            while x <= x_max and y_min <= y:
                x, y, v_x, v_y = step(x, y, v_x, v_y)
                max_y = max(y, max_y)
                if (x_min <= x <= x_max) and (y_min <= y <= y_max):
                    results.append(
                        {
                            "v_x_start": v_x_start,
                            "v_y_start": v_y_start,
                            "x_last": x,
                            "y_last": y,
                            "max_y": max_y,
                        }
                    )
                    break 
    return results

"""
results = check(target_area)
maximum = max(results, key=itemgetter("max_y"))
print(f"Maximum y: {maximum}")
# Maximum y: {'v_x_start': 11, 'v_y_start': 197, 'x_last': 66, 'y_last': -198, 'max_y': 19503}
"""

# Part 2
print("\nPart 2:")

"""
x_min, x_max = 20, 30
y_min, y_max = -10, -5
target_area = (x_min, x_max, y_min, y_max)
"""

def check(target_area):
    x_min, x_max, y_min, y_max = target_area

    # Determine minimal horizontal start velocity (v_x_start)
    v_x_min = ceil(sqrt(2 * x_min + 0.25) - 0.5)

    results = []
    for v_x_start in range(v_x_min, x_max + 1):
        for v_y_start in range(y_min, 197 + 1):
            x, y, v_x, v_y = 0, 0, v_x_start, v_y_start
            max_y = 0
            while x <= x_max and y_min <= y:
                x, y, v_x, v_y = step(x, y, v_x, v_y)
                if (x_min <= x <= x_max) and (y_min <= y <= y_max):
                    results.append(
                        {
                            "v_x_start": v_x_start,
                            "v_y_start": v_y_start,
                            "x_last": x,
                            "y_last": y,
                        }
                    )
                    break 
    return results


"""
results = check(target_area)
pprint(results)
print(len(results))
# 5200
"""
