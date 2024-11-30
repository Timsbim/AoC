# --------------------------------------------------------------------------- #
#    Day 13                                                                   #
# --------------------------------------------------------------------------- #
import re
from pprint import pprint


DAY = 13
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

pat = r"([^ ]+) would ([^ ]+) (\d+) happiness units by sitting next to ([^.]+)"
re_next_to = re.compile(pat)
with open(file_name, "r") as file:
    pairs = {}
    for line in file:
        person, sign, units, neighbour = re_next_to.match(line).groups()
        units = int(("" if sign == "gain" else "-") + units)
        pairs.setdefault(person, {})[neighbour] = units
if EXAMPLE:
    pprint(pairs)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def seatings(pairs):
    family = set(pairs)
    size = len(family)
    base = family.pop()
    seatings = [(base,)]
    while seatings:
        seating = seatings.pop()
        for person in family.difference(seating):
            new_seating = seating + (person,)
            if len(new_seating) == size:
                yield new_seating
            else:
                seatings.append(new_seating)


def happiness(pairs, seating):
    first, last = seating[0], seating[-1]
    happiness = pairs[first][last] + pairs[last][first]
    for left, right in zip(seating, seating[1:]):
        happiness += pairs[left][right] + pairs[right][left]
    return happiness

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(pairs):
    return max(happiness(pairs, seating) for seating in seatings(pairs))


solution = part_1(pairs)
if not EXAMPLE:
    assert solution == 618
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(pairs):
    family = pairs.keys()
    pairs = {
        person: happiness | {"Me": 0} for person, happiness in pairs.items()
    }
    pairs["Me"] = dict.fromkeys(family, 0)
    return max(happiness(pairs, seating) for seating in seatings(pairs))


solution = part_2(pairs)
if not EXAMPLE:
    assert solution == 601
print(solution)
