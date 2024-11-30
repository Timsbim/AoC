# --------------------------------------------------------------------------- #
#    Day 15                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 15
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    ingredients = []
    for line in file:
        metrics = line.split(": ")[1].split(", ")
        metrics = (int(metric.split()[1]) for metric in metrics)
        ingredients.append(tuple(map(int, metrics)))

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def get_weights(slots, row_sum=100):
    if slots == 1:
        yield (row_sum,)
    else:
        for n in range(row_sum + 1):
            for row in get_weights(slots - 1, row_sum - n):
                yield (n,) + row


def score(properties, weights):
    score = 1
    for property in properties:
        sub_score = sum(p * w for p, w in zip(property, weights))
        if sub_score <= 0:
            return 0
        score *= sub_score
    return score

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(ingredients):
    slots = len(ingredients)
    properties = tuple(zip(*(ingredient[:-1] for ingredient in ingredients)))
    return max(score(properties, weights) for weights in get_weights(slots))


solution = part_1(ingredients)
assert solution == (62842880 if EXAMPLE else 222870)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def total_calories(calories, weights):
    return sum(c * w for c, w in zip(calories, weights))


def part_2(ingredients):
    slots = len(ingredients)
    properties = tuple(zip(*(ingredient[:-1] for ingredient in ingredients)))
    calories = tuple(ingredient[-1] for ingredient in ingredients)
    return max(
        score(properties, weights)
        for weights in get_weights(slots)
        if total_calories(calories, weights) == 500
    )


solution = part_2(ingredients)
assert solution == (57600000 if EXAMPLE else 117936)
print(solution)
