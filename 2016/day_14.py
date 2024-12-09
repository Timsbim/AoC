# --------------------------------------------------------------------------- #
#    Day 14                                                                   #
# --------------------------------------------------------------------------- #
import re
from hashlib import md5
from pprint import pprint


DAY = 14
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

BASE = md5(("abc" if EXAMPLE else "yjdafjpo").encode())

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

RE_TRIPLE = re.compile(r"(.)\1\1")


def search():
    n, count, hashes = 0, 0, {}
    while True:
        string = hashes[n] if n in hashes else hash_it(n)
        if m := RE_TRIPLE.search(string):
            fivelet = m[0][0] * 5
            for m in range(n + 1, n + 1001):
                string = hashes.get(m)
                if string is None:
                    string = hashes.setdefault(m, hash_it(m))
                if fivelet in string:
                    count += 1
                    if count == 64:
                        return n
                    break
        n += 1
    return n    


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def hash_it(n):
    h = BASE.copy()
    h.update(str(n).encode())
    return h.hexdigest()


print(solution := search())
assert solution == (22728 if EXAMPLE else 25427)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="", flush=True)


def hash_it(n):
    h = BASE.copy()
    h.update(str(n).encode())
    string = h.hexdigest()
    for _ in range(2016):
        string = md5(string.encode()).hexdigest()
    return string


print(solution := search())
assert solution == (22551 if EXAMPLE else 22045)
