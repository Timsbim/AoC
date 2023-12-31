# --------------------------------------------------------------------------- #
#    Day 22                                                                   #
# --------------------------------------------------------------------------- #

from pprint import pprint
from itertools import product
from math import prod

DAY = 22
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2021/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    data = []
    for line in file:
        switch, coordinates = line.strip().split()
        coordinates = tuple(
            tuple(int(number) for number in coordinate[2:].split(".."))
            for coordinate in coordinates.split(",")
        )
        data.append((switch, coordinates))

pprint(data)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

cubes = set()
for switch, coordinates in data:
    new_cubes = set(
        product(
            *(
                range(max(-50, start), min(50, end) + 1)
                for start, end in coordinates
            )
        )
    )
    if switch == "on":
        cubes |= new_cubes
    else:
        cubes -= new_cubes
print(len(cubes)) # 647062

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")


def common_range(range_1, range_2):
    return (max(range_1[0], range_2[0]), min(range_1[1], range_2[1]))


def common_cuboid(cuboid_1, cuboid_2):
    return tuple(
        common_range(range_1, range_2)
        for range_1, range_2 in zip(cuboid_1, cuboid_2)
    )


def empty(cuboid):
    return any(stop < start for start, stop in cuboid)


def partition_range(range_, subrange):
    start, end = range_
    sub_start, sub_end = subrange
    ranges = []
    if start < sub_start:
        ranges.append((start, sub_start - 1))
    ranges.append((sub_start, sub_end))
    if sub_end < end:
        ranges.append((sub_end + 1, end))
    return tuple(ranges)


def remove_subcuboid(cuboid, subcuboid):
    return set(
        product(
            *(
                partition_range(range_, subrange)
                for range_, subrange in zip(cuboid, subcuboid)
            )
        )
    ) - {subcuboid}


def add_cuboids(cuboid_1, cuboid_2):
    subcuboid = common_cuboid(cuboid_1, cuboid_2)
    if empty(subcuboid):
        return {cuboid_2}
    return remove_subcuboid(cuboid_2, subcuboid)

def size(cuboid):
    return prod((end - start + 1) for start, end in cuboid)


def how_much_on(data):
    cuboids = set()
    for switch, cuboid in data:
        new_cuboids = set()
        if switch == "on":
            new_cuboids.add(cuboid)
            for cuboid_1 in cuboids:
                new_cuboids = set().union(
                    *(
                        add_cuboids(cuboid_1, cuboid_2)
                        for cuboid_2 in new_cuboids
                    )
                )
            cuboids |= new_cuboids
        else:
            cuboids = set().union(
                *(
                    add_cuboids(cuboid, cuboid_2)
                    for cuboid_2 in cuboids
                )
            )
    return sum(
        size(cuboid) for cuboid in cuboids
    )


on = how_much_on(data) # 1319618626668022
print(f"On: {on}!")
with open("output.txt", "w") as file:
    file.write(str(on)
