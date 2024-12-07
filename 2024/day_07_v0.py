# --------------------------------------------------------------------------- #
#    Day 7                                                                    #
# --------------------------------------------------------------------------- #
from functools import partial
from operator import add, mul
from pprint import pprint


DAY = 7
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2024/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    equations = []
    for line in file:
        test, numbers = line.split(": ")
        equations.append((int(test), tuple(map(int, numbers.split()))))
equations = tuple(equations)
if EXAMPLE:
    pprint(equations)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #


def solve(ops, test, numbers):
    """All numbers have length > 1, so no handling of length <= 1 necessary"""
    length, stack = len(numbers), [(1, numbers[0])]
    while stack:
        i, res0 = stack.pop()
        n, i = numbers[i], i + 1
        for op in ops:
            res1 = op(res0, n)
            if i == length:
                if res1 == test:
                    return True
            elif res1 <= test:
                stack.append((i, res1))
    return False


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(equations):
    check = partial(solve, (add, mul))
    return sum(test for test, numbers in equations if check(test, numbers))


print(solution := part_1(equations))
assert solution == (3749 if EXAMPLE else 1038838357795)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(equations):
    def concat(n, m): return int(f"{n}{m}")
    check = partial(solve, (add, mul, concat))
    return sum(test for test, numbers in equations if check(test, numbers))


print(solution := part_2(equations))
assert solution == (11387 if EXAMPLE else 254136560217241)
