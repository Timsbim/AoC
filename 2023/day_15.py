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

file_name = f"2023/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    words = file.read().strip().split(",")
if EXAMPLE:
    pprint(words)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def hashing(word):
    value = 0
    for char in word:
        value = ((value + ord(char)) * 17) % 256
    return value

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(words):
    return sum(map(hashing, words))


solution = part_1(words)
assert solution == (1320 if EXAMPLE else 514025)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(words):
    boxes = {}
    for word in words:
        if word.endswith("-"):
            label = word.rstrip("-")
            if (box := boxes.get(hashing(label), False)) and label in box:
                del box[label]
        else:
            label, length = word.split("=")
            box = boxes.setdefault(hashing(label), {})
            box[label] = int(length)
    
    return sum(
        (n + 1) * sum(
            slot * length
            for slot, length in enumerate(box.values(), start=1)
        )
        for n, box in boxes.items()
    )


solution = part_2(words)
assert solution == (145 if EXAMPLE else 244461)
print(solution)
