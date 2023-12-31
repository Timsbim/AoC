# --------------------------------------------------------------------------- #
#    Day 11                                                                   #
# --------------------------------------------------------------------------- #
import re
from pprint import pprint
from string import ascii_lowercase as ALPHABET


DAY = 11
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

old_password = "abcdefgh" if EXAMPLE else "hxbxwxba"

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

INCREMENT = dict(zip(ALPHABET, ALPHABET[1:] + "a"))


def increment(password):
    password = list(password)
    i = 8
    while i > 0:
        i -= 1
        char = password[i]
        password[i] = INCREMENT[char]
        if char != "z":
            break
    return "".join(password)


straights = (i for i in range(24) if i < 6 or 14 < i)
re_straight_3 = re.compile("|".join(ALPHABET[i:i + 3] for i in straights))
re_exclude = re.compile(r"[ilo]")
re_pairs = re.compile(r"(.)\1")


def valid(password):
    if bool(re_exclude.search(password)):
        return False
    if not bool(re_straight_3.search(password)):
        return False
    pairs = set(re_pairs.findall(password))
    if len(pairs) < 2:
        return False
    return True


def next_password(password):
    while True:
        if valid(password := increment(password)):
            return password

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

new_password = next_password(old_password)
if not EXAMPLE:
    assert new_password == "hxbxxyzz"
print(new_password)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

new_password = next_password(new_password)
if not EXAMPLE:
    assert new_password == "hxcaabcc"
print(new_password)
