# --------------------------------------------------------------------------- #
#    Day 7                                                                    #
# --------------------------------------------------------------------------- #
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


def solve(ops, test, numbers, res):        
    n, *numbers = numbers
    if len(numbers) == 0:
        return any(op(res, n) == test for op in ops)
    return any(solve(ops, test, numbers, op(res, n)) for op in ops)


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(equations):
    ops = add, mul
    return sum(test for test, (n, *ns) in equations if solve(ops, test, ns, n))


print(solution := part_1(equations))
assert solution == (3749 if EXAMPLE else 1038838357795)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(equations):
    def concat(n, m): return int(f"{n}{m}")
    ops = add, mul, concat
    return sum(test for test, (n, *ns) in equations if solve(ops, test, ns, n))


print(solution := part_2(equations))
assert solution == (11387 if EXAMPLE else 254136560217241)
