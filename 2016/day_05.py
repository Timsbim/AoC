# --------------------------------------------------------------------------- #
#    Day 5                                                                    #
# --------------------------------------------------------------------------- #
from hashlib import md5
from pprint import pprint


DAY = 5
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

ID = "abc" if EXAMPLE else "ugkcyxxp"

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(ID):
    i, pwd = 0, ""
    while True:
        h = md5()
        h.update(f"{ID}{i}".encode())
        string = h.hexdigest()
        if string.startswith("00000"):
            pwd += string[5]
            if len(pwd) == 8:
                return pwd
        i += 1


print(solution := part_1(ID))
assert solution == ("18f47a30" if EXAMPLE else "d4cd2ee1")

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(ID):
    i, count, pwd = 0, 0, [""] * 8
    while True:
        h = md5()
        h.update(f"{ID}{i}".encode())
        string = h.hexdigest()
        if string.startswith("00000"):
            index = int(string[5], base=16)
            if 0 <= index <= 7 and pwd[index] == "":
                pwd[index] = string[6]
                count += 1
                if count == 8:
                    return "".join(pwd)
        i += 1


print(solution := part_2(ID))
assert solution == ("05ace8e3" if EXAMPLE else "f2c730e5")