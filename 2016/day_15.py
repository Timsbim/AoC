# --------------------------------------------------------------------------- #
#    Day 15                                                                   #
# --------------------------------------------------------------------------- #
from math import prod


DAY = 15
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
    discs = []
    for line in file:
        row = line.split()
        discs.append((int(row[3]), int(row[-1][:-1])))
discs = tuple(discs)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def inv_mod(a, b):
    if b == 1:
        return 1

    r0, r1 = a, b
    s0, s1 = 1, 0
    while r1 > 0:
        d, r = divmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, s0 - d * s1

    return s0 if s0 >= 0 else s0 + b


def CRT(bs, ns):
    pns = prod(ns)
    nps = tuple(pns // n for n in ns)

    return sum(b * np * inv_mod(np, n) for b, np, n in zip(bs, nps, ns)) % pns


def solve(discs):
    """Let
        n  := number of discs
        pi := positions of disc i,
        qi := position of disc i at time = 0,
        ts := start time
    
    then a solution corresponds to the following system of equations:
    
        q1 + 1 + ts ≡ 0 (mod p1)
        q2 + 2 + ts ≡ 0 (mod p2)
                ...
        qn + n + ts ≡ 0 (mod pn)
    
    i.e.
    
        ts ≡ -(q1 + 1) (mod p1)
        ts ≡ -(q2 + 2) (mod p2)
                ...
        ts ≡ -(qn + n) (mod pn)
    
    which can be solved by the chinese remainder theorem.
    """
    bs = tuple(-(q + n) % p for n, (p, q) in enumerate(discs, 1))
    ns = tuple(p for p, _ in discs)
    
    return CRT(bs, ns)


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

print(solution := solve(discs))
assert solution == (5 if EXAMPLE else 121834)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

print(solution := solve(discs + ((11, 0),)))
assert solution == (85 if EXAMPLE else 3208099)
