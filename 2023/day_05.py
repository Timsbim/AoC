# --------------------------------------------------------------------------- #
#    Day 5                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 5
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

maps = []
with open(file_name, "r") as file:
    seeds = list(map(int, next(file).split(":")[1].split()))
    for line in file:
        line = line.strip()
        if line.endswith("map:"):
            maps.append([])
        elif line != "":
            start_d, start_s, length = map(int, line.split())
            maps[-1].append((start_s, start_s + length, start_d - start_s))
maps = [sorted(mapping) for mapping in maps]

if EXAMPLE:
    print(seeds)
    pprint(maps)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    minimum = float("inf")
    for seed in seeds:
        for mapping in maps:
            for start, end, offset in mapping:
                if start <= seed < end:
                    seed += offset
                    break
        if seed < minimum:
            minimum = seed
    return minimum


solution = part_1()
assert solution == (35 if EXAMPLE else 88151870)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def map_range(mapping, start_in, end_in):
    ranges = []
    if start_in < (start := mapping[0][0]):
        ranges.append((start_in, start))
    for start, end, offset in mapping:
        if start_in <= start:
            if end_in <= end:
                ranges.append((start + offset, end_in + offset))
                return ranges
            else:
                ranges.append((start + offset, end + offset))
        elif start_in < end:
            if end_in <= end:
                ranges.append((start_in + offset, end_in + offset))
                return ranges
            else:
                ranges.append((start_in + offset, end + offset))
    if (end := mapping[-1][1]) < end_in:
        if start_in <= end:
            ranges.append((end, end_in))
        else:
            ranges.append((start_in, end_in))
    return ranges


def part_2():
    minimum = float("inf")
    for i in range(0, len(seeds), 2):
        start, length = seeds[i:i + 2]
        ranges = [(start, start + length)]
        for mapping in maps:
            ranges = [
                range
                for start, end in ranges
                for range in map_range(mapping, start, end)
            ]
        minimum = min(minimum, min(start for start, _ in ranges))
    return minimum


solution = part_2()
assert solution == (46 if EXAMPLE else 2008785)
print(solution)
