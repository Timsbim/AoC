# --------------------------------------------------------------------------- #
#    Day 9                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 9
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    distances = {}
    for line in file:
        locations, distance = line.split(" = ")
        loc_from, loc_to = locations.split(" to ")
        distance = int(distance)
        distances.setdefault(loc_from, {})[loc_to] = distance
        distances.setdefault(loc_to, {})[loc_from] = distance
if EXAMPLE:
    pprint(distances)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(distances):
    graph = {loc: set(distances[loc]) for loc in distances}
    num_nodes = len(graph)
    min_dist = float("inf")
    for start in graph:
        pot_paths = [([start], 0)]
        while pot_paths:
            path, dist = pot_paths.pop()
            for node in graph[path[-1]]:
                if node not in path:
                    new_path = path + [node]
                    new_dist = dist + distances[path[-1]][node]
                    if new_dist >= min_dist:
                        continue
                    if len(new_path) == num_nodes:
                        min_dist = new_dist
                    else:
                        pot_paths.append((new_path, new_dist))
    return min_dist


solution = part_1(distances)
if not EXAMPLE:
    assert solution == 251
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

    
def part_2(distances):
    graph = {loc: set(distances[loc]) for loc in distances}
    num_nodes = len(graph)
    max_dist = 0
    for start in graph:
        pot_paths = [([start], 0)]
        while pot_paths:
            path, dist = pot_paths.pop()
            for node in graph[path[-1]]:
                if node not in path:
                    new_path = path + [node]
                    new_dist = dist + distances[path[-1]][node]
                    if len(new_path) == num_nodes:
                        if new_dist > max_dist:
                            max_dist = new_dist
                    else:
                        pot_paths.append((new_path, new_dist))
    return max_dist


solution = part_2(distances)
if not EXAMPLE:
    assert solution == 898
print(solution)
