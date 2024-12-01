# --------------------------------------------------------------------------- #
#    Day 9                                                                    #
# --------------------------------------------------------------------------- #
import re
from pprint import pprint


DAY = 9
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2016/input/day_{DAY:0>2}.txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

if not EXAMPLE:
    with open(file_name, "r") as file:
        compressed = file.read()

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

RE_MARKER = re.compile(r"\((\d+)x(\d+)\)")
assert compressed.count(" ") == 0

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

if EXAMPLE:
    compressed = "X(8x2)(3x3)ABCY"


def part_1(compressed):
    count = 0
    while m := RE_MARKER.search(compressed):
        start, end = m.start(), m.end()
        # Count (non-space) characters in sequence before marker
        count += start
        # Count marked length
        length, multiple = int(m[1]), int(m[2])
        count += length * multiple
        # Trim rest
        compressed = compressed[end+length:]
    # Count (non-space) characters in end piece and return
    return count + len(compressed)


print(solution := part_1(compressed))
assert solution == (18 if EXAMPLE else 110346)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

if EXAMPLE:
    compressed = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"


def part_2(compressed):
    count = 0
    while m := RE_MARKER.search(compressed):
        start, end = m.start(), m.end()
        # Count (non-space) characters in sequence before marker
        count += start
        # Count marked length (recursively)
        length, multiple = int(m[1]), int(m[2])
        count += multiple * part_2(compressed[end:end+length])
        # Trim rest
        compressed = compressed[end+length:]
    # Count (non-space) characters in end piece and return
    return count + len(compressed)


print(solution := part_2(compressed))
assert solution == (445 if EXAMPLE else 10774309173)
