# --------------------------------------------------------------------------- #
#    Day 19                                                                   #
# --------------------------------------------------------------------------- #

DAY = 19
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

ELVES = 5 if EXAMPLE else 3_014_603

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    stay = [*range(ELVES)]
    while (length := len(stay)) > 1:
        if length % 2:
            stay_new = [stay[-1]]
            stay_new.extend(stay[i] for i in range(0, length - 1, 2))
        else:
            stay_new = [stay[i]  for i in range(0, length - 1, 2)]
        stay = stay_new
    return stay.pop() + 1


print(solution := part_1())
assert solution == (3 if EXAMPLE else 1834903)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    if ELVES < 3:
        return 1
    i, n, delta = 2, 1, 2
    for i in range(3, ELVES + 1):
        n += delta
        if i == ELVES:
            return n
        if delta == 1 and n + n == i:
            delta = 2
        elif delta == 2 and n == i:
            delta, n = 1, 0


print(solution := part_2())
assert solution == (2 if EXAMPLE else 1420280)
