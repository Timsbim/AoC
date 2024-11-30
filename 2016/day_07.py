# --------------------------------------------------------------------------- #
#    Day 7                                                                    #
# --------------------------------------------------------------------------- #
import re
from pprint import pprint


DAY = 7
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2016/input/day_{DAY:0>2}"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

if not EXAMPLE:
    with open(f"{file_name}.txt", "r") as file:
        ips = [line.strip() for line in file]

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

RE_HYPER = re.compile(r"(?<=\[)[^\]]*")
RE_SUPER = re.compile(r"(?:^|\])([^\[$]*)")

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def supports_tls(ip):
    for m in RE_HYPER.finditer(ip):
        hyper = m[0]
        for i in range(len(hyper) - 3):
            if (hyper[i] == hyper[i+3]
                and hyper[i+1] == hyper[i+2]
                and hyper[i] != hyper[i+1]):
                return False
    for m in RE_SUPER.finditer(ip):
        super = m[1]
        for i in range(len(super) - 3):
            if (super[i] == super[i+3]
                and super[i+1] == super[i+2]
                and super[i] != super[i+1]):
                return True
    return False
    

def part_1(ips):
    return sum(supports_tls(ip) for ip in ips)


if EXAMPLE:
    with open(f"{file_name}_example_part_1.txt", "r") as file:
        ips = [line.strip() for line in file]
print(solution := part_1(ips))
assert solution == (2 if EXAMPLE else 105)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def supports_ssl(ip):
    abas = set()
    for m in RE_HYPER.finditer(ip):
        hyper = m[0]
        for i in range(len(hyper) - 2):
            if (hyper[i] == hyper[i+2] and hyper[i] != hyper[i+1]):
                abas.add(f"{hyper[i+1]}{hyper[i]}")
    for m in RE_SUPER.finditer(ip):
        super = m[1]
        for i in range(len(super) - 2):
            if (super[i] == super[i+2] and super[i] != super[i+1]):
                if f"{super[i]}{super[i+1]}" in abas:
                    return True
    return False


def part_2(ips):
    return sum(supports_ssl(ip) for ip in ips)


if EXAMPLE:
    with open(f"{file_name}_example_part_2.txt", "r") as file:
        ips = [line.strip() for line in file]
print(solution := part_2(ips))
assert solution == (3 if EXAMPLE else 258)
