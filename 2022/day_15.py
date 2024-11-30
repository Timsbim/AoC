# --------------------------------------------------------------------------- #
#    Day 15                                                                   #
# --------------------------------------------------------------------------- #

import re
from bisect import insort

DAY = 15
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/input/day_{DAY:0>2}"
row, grid_max = 2_000_000, 4_000_000
if EXAMPLE:
    file_name += "_example"
    row, grid_max = 10, 20
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_sensors(file_name):
    re_sensors = re.compile(
        r"^Sensor at x=(-?\d+), y=(-?\d+): "
        r"closest beacon is at x=(-?\d+), y=(-?\d+)$"
    )
    with open(file_name, "r") as file:
        for line in file:
            sx, sy, bx, by = map(int, re_sensors.match(line.rstrip()).groups())
            yield (sx, sy), (bx, by)

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def excluded_beacons(row, sensors):
    excluded, beacons = set(), set()
    for sensor, beacon in sensors:
        (sx, sy), (bx, by) = sensor, beacon
        if by == row:
            beacons.add(bx)
        dist = distance(sensor, beacon)
        if sy - dist <= row <= sy + dist:
            delta = dist - abs(sy - row)
            excluded.update(range(sx - delta, sx + delta + 1))
    return len(excluded - beacons)


print(excluded_beacons(row, get_sensors(file_name)))  # 5878678

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def max_interval(intervals):
    start, end = intervals[0]
    if 0 < start:
        return False
    for left, right in intervals[1:]:
        if left <= end < right:
            end = right
            if grid_max <= end:
                return True
    return False
    

def tuning_frequency(sensors):
    ranges = []
    for sensor, beacon in sensors:
        sy, dist = sensor[1], distance(sensor, beacon)
        ranges.append((sensor, (sy - dist, sy + dist), dist))
    for row in range(0, grid_max + 1):
        intervals = []
        for (sx, sy), (left, right), dist in ranges:
            if left <= row <= right:
                delta = dist - abs(sy - row)
                insort(intervals, (sx - delta, sx + delta))
        if not max_interval(intervals):
            missing = set(range(0, grid_max + 1))
            missing.difference_update(*(
                range(left, right + 1) for left, right in intervals
            ))
            return missing.pop() * 4_000_000 + row


sensors = get_sensors(file_name)
print(tuning_frequency(sensors))  # 11796491041245
