# --------------------------------------------------------------------------- #
#    Day 18                                                                   #
# --------------------------------------------------------------------------- #

from itertools import groupby
from operator import itemgetter

DAY = 18
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_blocks(file_name):
    with open(file_name, "r") as file:
        for line in file:
            yield tuple(map(int, line.rstrip().split(",")))

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

BASE_SIDES = [(1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1)]


def to_sides(block):
    x, y, z = (c * 2 for c in block)
    return {(bx + x, by + y, bz + z) for bx, by, bz in BASE_SIDES}

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def unconnected_sides(blocks):
    sides = set()
    for block in blocks:
        sides.symmetric_difference_update(to_sides(block))
    return sides


print(len(unconnected_sides(get_blocks(file_name))))  # 3576

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def scan_caves(blocks):
    dimensions = (0, 1), (0, 2), (1, 2)
    planes = {}
    for i, j in dimensions:
        k = ({0, 1, 2} - {i, j}).pop()
        sfunc, kfunc = itemgetter(i, j, k), itemgetter(i, j)
        planes[i, j] = set()
        for key, group in groupby(sorted(blocks, key=sfunc), key=kfunc):
            group = list(group)
            if len(group) == 1:
                continue
            start, end = group[0][k] + 1, group[-1][k]
            for n in set(range(start, end)) - {side[k] for side in group}:
                block = [0, 0, 0]
                block[i], block[j], block[k] = key[0], key[1], n
                planes[i, j].add(tuple(block))
    return planes[0, 1] & planes[0, 2] & planes[1, 2]


def is_connected(block1, block2):
    idx = [i for i in range(3) if block1[i] == block2[i]]
    if len(idx) < 2:
        return False
    if len(idx) == 3:
        return True
    k = ({0, 1, 2} - set(idx)).pop()
    return abs(block1[k] - block2[k]) == 1


def get_caves(blocks):
    scan = scan_caves(blocks)
    caves = []
    while scan:
        start = scan.pop()
        cave = set()
        extension = {start}
        while extension:
            cave.update(extension)
            next_extension = set()
            for block1 in extension:
                next_extension.update(
                    block2 for block2 in scan
                    if is_connected(block1, block2)
                )
            extension = next_extension
            scan.difference_update(extension)
        caves.append(cave)
    return caves


def get_surface(blocks):
    blocks = list(blocks)
    caves_sides = [unconnected_sides(cave) for cave in get_caves(blocks)]
    blocks_sides = unconnected_sides(blocks)
    return blocks_sides - {
        side
        for cave_sides in caves_sides if cave_sides <= blocks_sides
        for side in cave_sides
    }


surface = get_surface(get_blocks(file_name))
print(len(surface))  # 2066
