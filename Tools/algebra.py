from math import prod


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

