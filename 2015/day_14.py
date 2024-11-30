# --------------------------------------------------------------------------- #
#    Day 14                                                                   #
# --------------------------------------------------------------------------- #
import re
from pprint import pprint


DAY = 14
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

re_input = re.compile(r"([^ ]+)\D*(\d+)\D*(\d+)\D*(\d+)")
with open(file_name, "r") as file:
    reindeers = []
    for line in file:
        name, *durations = re_input.match(line).groups()
        velocity, flying, resting = map(int, durations)
        reindeers.append((name, velocity, flying, flying + resting))
if EXAMPLE:
    pprint(reindeers)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def distance(reindeer):
    seconds = 1_000 if EXAMPLE else 2503
    _, velocity, flying, total = reindeer
    full_cycles, rest = divmod(seconds, total)
    return velocity * (full_cycles * flying + min(flying, rest))


def part_1(reindeers):
    return max(distance(reindeer) for reindeer in reindeers)


solution = part_1(reindeers)
assert solution == (1120 if EXAMPLE else 2696)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def increment(reindeer, second):
    return reindeer[1] if (second % reindeer[3]) < reindeer[2] else 0


def part_2(reindeers):
    seconds = 1_000 if EXAMPLE else 2503
    distances = dict.fromkeys((name for name, *_ in reindeers), 0)
    scores = dict.fromkeys(distances, 0)
    for second in range(seconds):
        for reindeer in reindeers:
            distances[reindeer[0]] += increment(reindeer, second)
        max_distance = max(distances.values())
        for reindeer in reindeers:
            name = reindeer[0]
            if distances[name] == max_distance:
                scores[name] += 1
    return max(scores.values())


solution = part_2(reindeers)
assert solution == (689 if EXAMPLE else 1084)
print(solution)
