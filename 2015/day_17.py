# --------------------------------------------------------------------------- #
#    Day 17                                                                   #
# --------------------------------------------------------------------------- #
from collections import Counter, defaultdict
from itertools import product
from math import comb, prod


DAY = 17
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    containers = Counter(map(int, file))

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def combinations(containers, target):
    volumnes, max_counts = tuple(containers), tuple(containers.values())
    combinations = defaultdict(int)
    for counts in product(*(range(count + 1) for count in max_counts)):
        total_volumne = total_count = 0
        match = 0, True
        for volumne, count in zip(containers, counts):
            total_volumne += volumne * count
            if total_volumne > target:
                match = False
                break
            total_count += count
        if match and total_volumne == target:
            num_combinations = prod(
                comb(max_count, count)
                for count, max_count in zip(counts, max_counts)
                if count != 0
            )
            combinations[total_count] += num_combinations
    return combinations

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(containers, target):
    return sum(combinations(containers, target).values())


solution = part_1(containers, 25 if EXAMPLE else 150)
assert solution == (4 if EXAMPLE else 4372)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(containers, target):
    combs = combinations(containers, target)
    minimum = min(combs.values())
    return sum(
        count for count, num_combs in combs.items() if num_combs == minimum
    )


solution = part_2(containers, 25 if EXAMPLE else 150)
assert solution == (3 if EXAMPLE else 4)
print(solution)
