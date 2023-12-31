# --------------------------------------------------------------------------- #
#    Day 24                                                                   #
# --------------------------------------------------------------------------- #
from itertools import combinations
from math import gcd, prod
from pprint import pprint

import numpy as np


DAY = 24
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    hailstones = []
    for line in file:
        line = tuple(map(int, line.strip().replace(" @", ",").split(", ")))
        hailstones.append((line[:3], line[3:]))
HAILSTONES = tuple(hailstones)

if EXAMPLE:
    pprint(HAILSTONES)


def make_example(size=100, low=-1_000, high=1_000):
    rng = np.random.default_rng()
    
    p0, v0 = np.array([0, 0, 0]), rng.integers(low, high, 3)
    vs = rng.integers(low, high, (size, 3), endpoint=True)
    ns = np.cumsum(rng.integers(1, 100, size))
    rng.shuffle(ns)
    
    return tuple (
        (tuple(p0 + n * (v0 - vs[i])), tuple(vs[i]))
        for i, n in zip(rng.permutation(size), ns)
    )

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

INF = float("inf")


def intersection(hailstone_0, hailstone_1):
    (p00, p01), (v00, v01) = hailstone_0
    (p10, p11), (v10, v11) = hailstone_1
    b = np.array([p10 - p00, p11 - p01])
    a = np.array([[v00, -v10], [v01, -v11]])
    try:
        alpha, beta = np.linalg.solve(a, b)
        if alpha < 0 or beta < 0:
            return False
        return p00 + alpha * v00, p01 + alpha * v01
    except np.linalg.LinAlgError:
        if p00 == p10 or p01 == p11:
            return INF
        else:
            return False


def project(hailstone):
    p, v = hailstone
    return p[:2], v[:2]


LEFT  =  7 if EXAMPLE else 200_000_000_000_000
RIGHT = 27 if EXAMPLE else 400_000_000_000_000


def part_1():
    count = 0
    for h0, h1 in combinations(HAILSTONES, r=2):
        col = intersection(project(h0), project(h1))
        if col == INF:
            count += 1
        elif isinstance(col, tuple):
            x, y = col
            if LEFT <= x <= RIGHT and LEFT <= y <= RIGHT:
                count += 1

    return count


solution = part_1()
assert solution == (2 if EXAMPLE else 29142)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


# A solution p, v would satisfy
# 
#     p + ni * v = pi + ni * vi
#     
# which implies
#
#    p = pi mod (vi - v)
#
# for all pi, vi, and that looks like CRT-equations, one set for each
# dimension.
#
# The strategy: Solve the CRT-equation for each dimension individually for a
# range of potential vs (from -1_000 to 1_000 since all velocities are in this
# range - but that's just a guess), and then check if the solution leads to an
# overall solution.
# 
# I don't think that this guarantees a solution, though.
#
# Solutions were found:
#    - Example: second z-solution, after zero x/y-solutions
#    - Puzzle input: 102th y-solution, after 785 unsuccessful x-solutions


def inv_mod(a, b):
    """Positive inverse of a mod b if gcd(a, b) == 1:
    Using the extended Euclidian algorithm gives s and t with:
        1 = gcd(a, b) = s * a + t * b -> 1 = s * a mod b
    (see: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm).
    """
    if b == 1:
        return 1

    r0, r1 = a, b
    s0, s1 = 1, 0
    while r1 > 0:
        d, r = divmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, s0 - d * s1

    # abs(s0) < b -> b + s0 > 0 if s0 < 0 and b + s0 = s0 mod b
    return s0 if s0 >= 0 else s0 + b


def CRT(bs, ns):
    """Standard implmentation that produces minimal results (eg. see here:
    https://youtu.be/ru7mWZJlRQg?si=K-NzKm_81RpIU7qC).
    
    Requirements:
        - len(bs) == len(ns)
        - ns co-prime
        - 0 <= bs < ns
    """
    # Make sure that each equation can be solved in isolation
    pns = prod(ns)
    nps = tuple(pns // n for n in ns)
    
    return sum(b * np * inv_mod(np, n) for b, np, n in zip(bs, nps, ns)) % pns


def solve_1_dim(dim, limit):    
    # Projektion on the selected dimension 0, 1 or 2
    ps, vs = zip(*((p[dim], v[dim]) for p, v in HAILSTONES))

    # Testing of projected velocities (integer interval)
    for v0 in range(-limit, limit + 1):

        if v0 in vs:  # Won't work: unreachable points
            continue

        # Preparation for CRT:
        # -> Make sure 0 <= bs < ns (CRT requirement)
        ns = [v - v0 for v in vs]
        bs = [p % n for p, n in zip(ps, ns)]
        for i, (b, n) in enumerate(zip(bs, ns)):
            if n < 0:
                ns[i], bs[i] = -n, b - n
        # -> Make sure the ns are co-prime
        ns_valid = tuple(
            i
            for i, n0 in enumerate(ns)
            if all(gcd(n0, n1) == 1 for n1 in ns[i+1:])
        )
        bs = tuple(bs[i] for i in ns_valid)
        ns = tuple(ns[i] for i in ns_valid)

        # Apply CRT to solve the equation ...
        p0 = CRT(bs, ns)
        # ... and check if the solution provides a valid path (eg. a positve
        # integer-solution)
        ts, valid = [], True
        for p, v in zip(ps, vs):
            # p0 + t * v0 = p + t * v -> t = (p0 - p) / (v - v0)
            t = (p0 - p) / (v - v0) 
            if t <= 0 or int(t) != t:
                valid = False
                break
            ts.append(int(t))
        if not valid:
            continue
        yield tuple(ts)


def part_2(limit):
    ps, vs = zip(*HAILSTONES)

    # Go over x, y and z dimension
    for dim in range(3):

        # Try to expand a single dimensional solution to an overall solution
        for ts in solve_1_dim(dim, limit):

            # Take 2 arbitray times and calculate the candidate for the
            # velocity vector
            t0, t1 = ts[0], ts[1]
            v0 = tuple(
                ps[1][i] + t1 * vs[1][i] - ps[0][i] - t0 * vs[0][i]
                for i in range(3)
            )
            t = t1 - t0
            # Candidate is only viable if it consists of integers
            if any(int(v0[i] / t) != v0[i] / t for i in range(3)):
                continue
            v0 = tuple(int(v0[i] / t) for i in range(3))

            # Now calculate the corresponding origin candidate
            p0 = tuple(ps[0][i] + t0 * (vs[0][i] - v0[i]) for i in range(3))

            # And finally check if this provides a consistent solution
            if all(
                p0[i] + t * v0[i] == p[i] + t * v[i]
                for p, t, v in zip(ps, ts, vs)
                for i in range(3)
            ):
                return sum(p0)


solution = part_2(10 if EXAMPLE else 1_000)
assert solution == (47 if EXAMPLE else 848947587263033)
print(solution)


# Interestingly, one also gets solutions (for the example and my input) if
# this is done only once, over the set of equations provided by summing over
# the coordinates - much faster, of course.


def part_2_alt(limit):
    # Projektion on 1 dimension along planes of sum-invariance
    pss, vss = zip(*((sum(p), sum(v)) for p, v in HAILSTONES))

    # Testing of projected velocities (integer interval)
    for vs0 in range(-limit, limit + 1):

        if vs0 in vss:  # Won't work: unreachable points
            continue

        # Preparation for CRT:
        # -> Make sure 0 <= bs < ns (CRT requirement)
        ns = [vs - vs0 for vs in vss]
        bs = [ps % n for ps, n in zip(pss, ns)]
        for i, (b, n) in enumerate(zip(bs, ns)):
            if n < 0:
                ns[i], bs[i] = -n, b - n
        # -> Make sure the ns are co-prime
        ns_valid = tuple(
            i
            for i, n0 in enumerate(ns)
            if all(gcd(n0, n1) == 1 for n1 in ns[i+1:])
        )
        bs = tuple(bs[i] for i in ns_valid)
        ns = tuple(ns[i] for i in ns_valid)

        # Apply CRT to solve the equation ...
        ps0 = CRT(bs, ns)
        # ... and check if the solution provides a valid path (eg. a positve
        # integer-solution)
        if all( # ps0 + t * vs0 = ps + t * vs -> t = (ps0 - ps) / (vs - vs0)
            t > 0 and int(t) == t
            for t in ((ps0 - ps) / (vs - vs0) for ps, vs in zip(pss, vss))
        ):
            return ps0


print(f"Part 2: {part_2_alt(10 if EXAMPLE else 1_000)}")
