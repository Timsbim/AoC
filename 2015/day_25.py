# --------------------------------------------------------------------------- #
#    Day 25                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 25
EXAMPLE = True

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

# Enter the code at row 3010, column 3019.
ROW, COLUMN = (6, 5) if EXAMPLE else (3010, 3019)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #



# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="\n")

# 33554393 is prime => Z / (Z * 33554393) is a field
assert all(33554393 % n != 0 for n in range(2, 33554393 // 2 + 1))


value = 20151125
for n in range(1, 11):
    print(f"{n}: {value}")
    value = (value * 252533) % 33554393


def part_1():
    return None


print(solution := part_1())
# assert solution == (if EXAMPLE else)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return None


print(solution := part_2())
# assert solution == (if EXAMPLE else)

from math import prod


def inv_mod(a, b):
    """Positive inverse of a mod b if gcd(a, b) == 1:
    Using the extended Euclidian algorithm gives s and t with:
        1 = gcd(a, b) = s * a + t * b -> 1 = s * a mod b
    (see: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm).
    """
    if b == 1:
        return 1

    r0, r1 = a, b
    s0, s1 = 1, 0
    while r1 > 0:
        d, r = divmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, s0 - d * s1

    # abs(s0) < b -> b + s0 > 0 if s0 < 0 and b + s0 = s0 mod b
    return s0 if s0 >= 0 else s0 + b
