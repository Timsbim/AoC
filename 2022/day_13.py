# --------------------------------------------------------------------------- #
#    Day 13                                                                   #
# --------------------------------------------------------------------------- #

from ast import literal_eval
from itertools import zip_longest

DAY = 13
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_packet_pairs(file_name):
    with open(file_name, "r") as file:
        packet = []
        for line in file:
            line = line.strip()
            if line == "":
                yield packet
                packet = []
            else:
                packet.append(literal_eval(line))


def get_packets(file_name):
    yield from (part for pair in get_packet_pairs(file_name) for part in pair)
     
# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left != right:
            return -1 if left < right else 1
        return 0
    if isinstance(left, int):        
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])
    for left, right in zip_longest(left, right):
        if left is None:
            return -1
        if right is None:
            return 1
        res = compare(left, right)
        if res != 0:
            return res
    return 0


def in_order(left, right):
    return compare(left, right) <= 0

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

packet_pairs = get_packet_pairs(file_name)
io_idx = (n for n, (l, r) in enumerate(packet_pairs, 1) if in_order(l, r))
print(sum(io_idx))  # 5198

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

dividers = [[[2]], [[6]]]
packets = list(get_packets(file_name)) + dividers
i, j = (
    sum(compare(packet, d) == -1 for packet in packets) + 1 for d in dividers
)
print(i * j)  # 22344
