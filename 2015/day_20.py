# --------------------------------------------------------------------------- #
#    Day 20                                                                   #
# --------------------------------------------------------------------------- #
from functools import cache
from itertools import product
from math import prod
from pprint import pprint


DAY = 20

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

NUMBER = 36_000_000

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def prime_sieve(number):
    if number == 2:
        return (2,)
    
    primes = [2]
    sieve = tuple(range(3, number + 1, 2))
    while sieve:
        p = sieve[0]
        primes.append(p)
        includes = dict.fromkeys(sieve[1:], True)
        for n in range(2 * p, sieve[-1] + 1, p):
            includes[n] = False
        sieve = tuple(n for n, take in includes.items() if take)
    
    return tuple(primes)


def factorization(n):
    factors = Counter()
    p = 2
    while n > 1:
        d, r = divmod(n, p)
        if r == 0:
            factors[p] += 1
            n = d
        else:
            p += 1
    
    return factors

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def start():
    primes = prime_sieve(100)
    f = 1
    pp = 1
    for p in primes:
        if pp >= NUMBER // 10:
            return int(NUMBER // 10 / f)
        f *= p / (p - 1)
        pp *= p


def num_presents(factors):
    return prod((p ** (k + 1) - 1) // (p - 1) for p, k in factors.items())


def part_1():
    for nr in range(start(), NUMBER):
        presents = sum(n for n in range(1, nr + 1) if nr % n == 0)
        if presents * 10 >= NUMBER:
            return nr


solution = part_1()
assert solution == 831_600
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(start):
    for nr in range(start, NUMBER):
        presents = sum(n for n in range(nr - 49, nr + 1) if nr % n == 0) * 11
        if presents >= NUMBER:
            return nr


solution = part_2(solution)
assert solution == 884_520
print(solution)
