# --------------------------------------------------------------------------- #
#    Day 1                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 1
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2016/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    directions = [(d[0], int(d[1:])) for d in file.read().split(", ")]

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(directions):
    d, n = directions[0]
    h, v, o = n if d == 'R' else -n, 0, 'E' if d == 'R' else 'W'
    for i, (d, n) in enumerate(directions[1:]):
        if i % 2:
            if (o == 'N' and d == 'R') or (o == 'S' and d == 'L'):
                h += n
                o = 'E'
            else:
                h -= n
                o = 'W'
        else:
            if (o == 'E' and d == 'L') or (o == 'W' and d == 'R'):
                v += n
                o = 'N'
            else:
                v -= n
                o = 'S'
 
    return abs(h) + abs(v)
 

print(solution := part_1(directions))
assert solution == (8 if EXAMPLE else 300)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(directions):
    d, n = directions[0]
    delta, o = 1 if d == 'R' else -1, 'E' if d == 'R' else 'W'
    p, visited = (0, 0), {(0, 0)}
    for _ in range(n):
        visited.add(p := (p[0] + delta, p[1]))
    for i, (d, n) in enumerate(directions[1:]):
        if i % 2:
            if (o == 'N' and d == 'R') or (o == 'S' and d == 'L'):
                delta, o = 1, 'E'
            else:
                delta, o = -1, 'W'
            for _ in range(n):
                p = (p[0] + delta, p[1])
                if p in visited:
                    return abs(p[0]) + abs(p[1])
                visited.add(p)
        else:
            if (o == 'E' and d == 'L') or (o == 'W' and d == 'R'):
                delta, o = 1, 'N'
            else:
                delta, o = -1, 'S'
            for _ in range(n):
                p = (p[0], p[1] + delta)
                if p in visited:
                    return abs(p[0]) + abs(p[1])
                visited.add(p)
    return visited
 

print(solution := part_2(directions))
assert solution == (12 if EXAMPLE else 159)
