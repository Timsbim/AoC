# --------------------------------------------------------------------------- #
#    Day 19                                                                   #
# --------------------------------------------------------------------------- #
import pickle
from pprint import pprint
from itertools import combinations, permutations, product


DAY = 19
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

def get_scanners(file_name):
    scanners, counter = {}, -1
    with open(file_name, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("--- scanner"):
                counter += 1
                scanners[counter] = set()
            elif line != "":
                reading = tuple(int(number) for number in line.split(","))
                scanners[counter].add(reading)
    return scanners

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def mat_mul(matrix_1, matrix_2):
    """ Multiplicates 2 matrices without checking for adequate dimensions """
    result = []
    for row in matrix_1:
        new_row = []
        for col in zip(*matrix_2):
            new_row.append(sum(a * b for a, b in zip(row, col)))
        result.append(tuple(new_row))
    return tuple(result)


def transpose(matrix):
    return tuple(zip(*matrix))


def get_3d_cube_rotations():
    """ Builds all 3d cube rotation matrices"""
    # 1. Reflections sorted by determinant (+/-1)
    reflections = {-1: [], 1: [(1, 1, 1)]}
    for n in 1, 2, 3:  # Number of -1s in the diagonal
        reflections[(-1) ** n].extend(  # Determinant is -1^number of -1s
            tuple(-1 if i in minus else 1 for i in (0, 1, 2))
            for minus in combinations((0, 1, 2), n)
        )
    # 2. Take the permutaitions, get their determinant (-1^number of swaps)
    # and multiplicate them with the corresponding reflections
    rotations = []
    for p in permutations((0, 1, 2)):
        swaps = (i == p[j] and p[i] == j for i, j in ((0, 1), (0, 2), (1, 2)))
        for reflection in reflections[(-1) ** sum(swaps)]:
            rotation = tuple(
                tuple(r if j == i else 0 for j, r in enumerate(reflection))
                for i in p
            )
            rotations.append(rotation)
    return rotations
    
    
def print_rotation(rotation):
    for row in rotation:
        print(" ".join(f"{n:2> }" for n in row))


def rotate(rotation, reading):
    return tuple(sum(a * b for a, b in zip(row, reading)) for row in rotation)


def normalize_readings(readings):
    origin = readings[0]
    return [
        tuple(n - o for n, o in zip(reading, origin))
        for reading in readings
    ]

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def get_matches(scanners):
    rots = get_3d_cube_rotations()
    matches = {}
    for n, m in combinations(scanners, 2):
        reads_0, reads_1 = scanners[n], scanners[m]
        found = False
        for rot in rots:
            roted_0 = [rotate(rot, r) for r in reads_0]
            for r0, r1 in product(roted_0, reads_1):
                dx, dy, dz = r1[0] - r0[0], r1[1] - r0[1], r1[2] - r0[2]
                num = 0
                for r in roted_0:
                    if (r[0] + dx, r[1] + dy, r[2] + dz) not in reads_1:
                        continue
                    num += 1
                    if num == 12:
                        matches[n, m] = (rot, (dx, dy, dz))
                        rot = transpose(rot)
                        shift = rotate(rot, (-dx, -dy, -dz))
                        matches[m, n] = (rot, shift)
                        found = True
                        break
                if found:
                    break
            if found:
                break
    return matches


def build_graph(pairs):
    connects = {}
    for n, m in pairs:
        connects.setdefault(n, set()).add(m)
    return connects


def span_graph(graph):
    result = []
    start = min(graph.keys())
    paths = [[start]]
    while paths:
        path = paths.pop()
        stop = True
        for node in graph[path[-1]]:
            if node not in path:
                paths.append(path + [node])
                stop = False
        if stop:
            result.append(path)
    return result


scanners = get_scanners(file_name)
if EXAMPLE:
    matches = get_matches(scanners)
else:
    with open("2021/day_19_matches.pkl", "rb") as file:
        matches = pickle.load(file)
graph = build_graph(matches.keys())
paths = span_graph(graph)
if EXAMPLE:
    pprint(matches)
    pprint(graph)
    pprint(paths)


beacons = set()
for path in paths:
    path = list(reversed(path))
    source = path[0]
    path_beacons = scanners[source]
    for dest in path[1:]:
        rot, shift = matches[source, dest]
        path_beacons = scanners[dest] | {
            tuple(c + s for c, s in zip(rotate(rot, r), shift))
            for r in path_beacons 
        }
        source = dest
    beacons |= path_beacons
print(len(beacons))  # 400

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2: ", end="")


def manhattan(scanner_1, scanner_2):
    return sum(abs(scanner_1[i] - scanner_2[i]) for i in range(3))


scanners = {(0, 0, 0)}
for path in paths:
    path = list(reversed(path))
    source = path[0]
    scanner = (0, 0, 0)
    for dest in path[1:]:
        rot, shift = matches[source, dest]
        scanner = tuple(c + s for c, s in zip(rotate(rot, scanner), shift))
        source = dest
    scanners.add(scanner)
print(max(manhattan(s0, s1) for s0, s1 in combinations(scanners, 2)))  # 12168
