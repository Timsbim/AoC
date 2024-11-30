# --------------------------------------------------------------------------- #
#    Day 25                                                                   #
# --------------------------------------------------------------------------- #

from math import log

DAY = 25
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_snafus(file_name):
    with open(file_name, "r") as file:
        return file.read().splitlines()

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

SNAFUTRANS = {ord(s): ord(d) for s, d in zip("=-012", "01234")}
DIGIT_TO_SNAFU = {n: d for n, d in zip(range(-2, 3), "=-012")}


def snafu_to_decimal(snafu):
    return int(snafu.translate(SNAFUTRANS), 5) - (5 ** len(snafu) - 1) // 2


def to_fiver(number):
    if number == 0:
        return [0]
    max_n = int(log(number, 5))
    digits = []
    for n in range(max_n, -1, -1):
        digit, number = divmod(number, 5 ** n)
        digits.append(digit)
    return digits


def decimal_to_snafu(number):
    digits = to_fiver(number)
    rest = 0
    snafu = []
    while digits or rest:
        digit = rest
        if digits:
            digit += digits.pop()
        rest, digit = divmod(digit, 5)
        if digit <= 2:
            snafu.append(DIGIT_TO_SNAFU[digit])
        else:
            rest += 1
            snafu.append(DIGIT_TO_SNAFU[digit - 5])
    return "".join(reversed(snafu))


def decode(snafus):
    return decimal_to_snafu(sum(map(snafu_to_decimal, snafus)))

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="\n")

print(decode(get_snafus(file_name)))  # 2-2=12=1-=-1=000=222
