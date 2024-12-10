# --------------------------------------------------------------------------- #
#    Day 10                                                                   #
# --------------------------------------------------------------------------- #
DAY = 10
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2024/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    topos = {
        (r, c): n
        for r, line in enumerate(file)
        for c, n in enumerate(map(int, line.rstrip()))
    }

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #


def hike(topos):
    score = count = 0
    for (r0, c0), n in topos.items():
        if n: continue
        heads = [(r0, c0)]
        for n in range(1, 10):
            heads_new = []
            for r, c in heads:
                for dr, dc in (0, 1), (1, 0), (0, -1), (-1, 0):
                    r1, c1 = r + dr, c + dc
                    if topos.get((r1, c1), -1) == n:
                        heads_new.append((r1, c1))
            heads = heads_new
        score += len(set(heads))
        count += len(heads)
    return score, count


solution_1, solution_2 = hike(topos)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #

print(f"Part 1: {solution_1}")
assert solution_1 == (36 if EXAMPLE else 776)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #

print(f"Part 2: {solution_2}")
assert solution_2 == (81 if EXAMPLE else 1657)
