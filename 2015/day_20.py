# --------------------------------------------------------------------------- #
#    Day 20                                                                   #
# --------------------------------------------------------------------------- #
from functools import cache
from itertools import product
from math import prod
from pprint import pprint


DAY = 20
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

NUMBER = 3_600 if EXAMPLE else 36_000_000

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

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="\n")


@cache
def num_presents(factors):
    if len(factors) == 1:
        p, k = factors[0]
        return (p ** (k + 1) - 1) // (p - 1)
    return num_presents(factors[:1]) * num_presents(factors[1:])


def num_presents(factors):
    return prod((p ** (k + 1) - 1) // (p - 1) for p, k in factors.items())


def part_1(NUMBER):
    ps = prime_sieve(20)
    pprint(ps)
    
    l = 8
    ps = ps[:l]
    ks_max = []
    for p in ps:
        k, s = 0, 1
        while True:
            k += 1
            s = p * s + 1
            if s >= NUMBER:
                ks_max.append(k)
                break
    ks_max = tuple(ks_max)
    pprint(ks_max)
    
    minimum, ks_min = float("inf"), ks_max
    for ks in product(*(range(k_max + 1) for k_max in ks_max)):
        factors = dict(zip(ps, ks))
        if num_presents(factors) >= NUMBER:
            nr = prod(p ** k for p, k in factors.items())
            if nr < minimum:
                minimum = nr
                ks_min = ks
    
    return minimum, ks_min


# (2, 3, 5, 7, 11, 13, 17, 19)
# (25, 16, 11, 9, 8, 7, 7, 6)
# 7_927_920 (4, 2, 1, 1, 2, 1, 0, 0)

ps = prime_sieve(30)
ks = (4, 2, 1, 1, 2, 1)
assert 7_927_920 == prod(p ** k for p, k in zip(ps, ks))
assert NUMBER <= num_presents(dict(zip(ps, ks)))


#minimum, ks_min = part_1(NUMBER)
# assert solution == (if EXAMPLE else)  # 1_200_000, 3_984_120 <- too high
#print(f"{minimum:_}", ks_min)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return None


solution = part_2()
# assert solution == (if EXAMPLE else)
print(solution)


def part_1(NUMBER):
    maximum, max_n = float("-inf"), 0
    primes = [2, 3]
    for n in range(4, NUMBER + 1):
        m = n
        factors = {}
        for p in primes:
            k = 0
            while m != 1:
                d, r = divmod(m, p)
                if r != 0:
                    break
                k += 1
                m = d
            if k > 0:
                factors[p] = k
        if m > 1:
            primes.append(n)
            factors[m] = 1
        num = num_presents(factors)
        if num > maximum:
            print(f"{n:_}", f"{num:_}", f"{n - max_n:_}", f"{num - maximum:_}")
            maximum, max_n = num, n
        #if num_presents(tuple(factors.items())) * 10 >= NUMBER:
        #    return n


#part_1(1_000_000) =>  Solution: 831_600 

nr = 831600
print(sum(n for n in range(1, nr + 1) if nr % n == 0))

def part_2():
    for nr in range(51, NUMBER):
        presents = sum(n for n in range(nr - 49, nr + 1) if nr % n == 0) * 11
        if presents >= NUMBER:
            return nr

#print(part_2())

from collections import Counter

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


factors = factorization(nr)
pprint(factors)
assert nr == prod(p ** k for p, k in factors.items())


def part_2():
    maxi = float("-inf")
    for nr in range(1, NUMBER):
        presents = sum(
            n
            for n in range(max(1, nr // 50), nr + 1)
            if nr % n == 0
        )
        if maxi < presents:
            print(f"{nr:_}, {presents:_}")
            maxi = presents
        if presents * 11 >= NUMBER:
            return nr


print(part_2())
