# --------------------------------------------------------------------------- #
#    Day 22                                                                   #
# --------------------------------------------------------------------------- #
from collections import defaultdict
from itertools import groupby
from pprint import pprint

import heapq


DAY = 22
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
    BRICKS = [
        tuple(
            tuple(map(int, part.split(",")))
            for part in line.strip().split("~")
        )
        for line in file
    ]
if EXAMPLE:
    pprint(BRICKS)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def blocks(brick):
    (x0, y0, z0), (x1, y1, z1) = brick
    if x0 < x1:
        yield from ((x, y0, z0) for x in range(x0, x1 + 1))
    elif y0 < y1:
        yield from ((x0, y, z0) for y in range(y0, y1 + 1))
    elif z0 < z1:
        yield from ((x0, y0, z) for z in range(z0, z1 + 1))
    else:
        yield x0, y0, z0


def floor(brick):
    z0 = brick[0][2]
    yield from ((x, y) for x, y, z in blocks(brick) if z == z0)


def build_support():
    supported = defaultdict(set)
    
    settled, planes, block_to_brick = [], defaultdict(set), {}
    def key(brick):
        return brick[0][2]

    for z0, layer in groupby(sorted(BRICKS, key=key), key=key):
    
        for brick in layer:
    
            z_dest = z0
            for z in range(z0 - 1, 0, -1):
                if any(block in planes[z] for block in floor(brick)):
                    break
                z_dest = z
            if z_dest < z0:
                offset = z0 - z_dest
                (x0, y0, z0), (x1, y1, z1) = brick
                brick = (x0, y0, z0 - offset), (x1, y1, z1 - offset)
            settled.append(brick)
    
            for x, y, z in blocks(brick):
                planes[z].add((x, y))
                if z == z_dest and (x, y) in planes[z-1]:
                    supported[brick].add(block_to_brick[x, y, z-1])
                block_to_brick[x, y, z] = brick
            
    supporting = defaultdict(set)
    for brick_0 in settled:
        supporting[brick_0] = set()
        for brick_1 in supported[brick_0]:
            supporting[brick_1].add(brick_0)
   
    return supported, supporting


def identify_unsafes(supported, supporting):
    bricks = set().union(*supported.values()) | supported.keys()
    unsafe = set()
    for brick_0 in bricks:
        for brick_1 in supporting[brick_0]:
            if len(supported[brick_1]) == 1:
                unsafe.add(brick_0)
                break

    return unsafe


def part_1():
    supported, supporting = build_support()
    unsafe = identify_unsafes(supported, supporting)
    return len(BRICKS) - len(unsafe)


solution = part_1()
assert solution == (5 if EXAMPLE else 434)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    supported, supporting = build_support()
    unsafe = identify_unsafes(supported, supporting)
    
    def key(brick):
        return brick[1][2]

    count = 0
    for start in unsafe:
        heap = [(1, start)]
        heapq.heapify(heap)
        disintegrated = {start}
        while heap:
            _, path = heapq.heappop(heap)
            for brick in supporting[path]:
                if len(supported[brick] - disintegrated) == 0:
                    heapq.heappush(heap, (key(brick), brick))
                    disintegrated.add(brick)
        count += len(disintegrated) - 1
   
    return count


solution = part_2()
assert solution == (7 if EXAMPLE else 61209)
print(solution)
