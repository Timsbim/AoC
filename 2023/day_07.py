# --------------------------------------------------------------------------- #
#    Day 7                                                                    #
# --------------------------------------------------------------------------- #
from collections import Counter
from pprint import pprint


DAY = 7
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    players = []
    for line in file:
        cards, bid = line.split()
        players.append((cards, int(bid)))
if EXAMPLE:
    pprint(players)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

CARDS = {card: value for value, card in enumerate("23456789TJQKA")}
TYPES = {
    (1, 1, 1, 1, 1): 1, (1, 1, 1, 2): 2, (1, 2, 2): 3,
    (1, 1, 3): 4, (2, 3): 5, (1, 4): 6, (5,): 7
}


def get_type(cards):
    if PART == 2 and "J" in cards and cards != "JJJJJ":
        card = Counter(cards.replace("J", "")).most_common()[0][0]
        cards = cards.replace("J", card)
    return tuple(sorted(Counter(cards).values()))


def key(cards):
    return (TYPES[get_type(cards)], *(CARDS[c] for c in cards))


def winnings(players):
    players = sorted(players, key=lambda p: key(p[0]))
    return sum(n * bid for n, (_, bid) in enumerate(players, start=1))

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

PART = 1
solution = winnings(players)
assert solution == (6440 if EXAMPLE else 251216224)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

PART = 2
CARDS["J"] = -1
solution = winnings(players)
assert solution == (5905 if EXAMPLE else 250825971)
print(solution)
