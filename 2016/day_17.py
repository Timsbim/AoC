# --------------------------------------------------------------------------- #
#    Day 17                                                                   #
# --------------------------------------------------------------------------- #
from hashlib import md5


DAY = 17
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

BASE = md5(("kglvqrro" if EXAMPLE else "hhhxzeay").encode())

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

OPEN = {"b", "c", "d", "e", "f"}
DELTA = (-1, 0), (1, 0), (0, -1), (0, 1)
MOVE = "UDLR"
MOVEB = "U".encode(), "D".encode(), "L".encode(), "R".encode()


def solve(shortest=True):
    max_path, stack = 0, [(0, 0, "", BASE)]
    while stack:
        stack_new = []
        for r, c, path, h in stack:
            for i, char in enumerate(h.hexdigest()[:4]):
                if char not in OPEN:
                    continue
                dr, dc = DELTA[i]
                if 0 <= (r1 := r + dr) < 4 and 0 <= (c1 := c + dc) < 4:
                    path1 = path + MOVE[i]
                    if r1 == 3 and c1 == 3:
                        if shortest:
                            return path1
                        else:
                            max_path = len(path1)
                            continue
                    h1 = h.copy()
                    h1.update(MOVEB[i])
                    stack_new.append((r1, c1, path1, h1))
        stack = stack_new
    return max_path


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

print(solution := solve())
assert solution == ("DDUDRLRRUDRD" if EXAMPLE else "DDRUDLRRRD")

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

print(solution := solve(False))
assert solution == (492 if EXAMPLE else 398)
