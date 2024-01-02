# --------------------------------------------------------------------------- #
#    Day 21                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 21
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

SHOP = {
    "Damage": {
        4: 8,
        5: 10,
        6: 25,
        7: 40,
        8: 74,
    },
    "Armor": {
        0: 0,
        1: 13,
        2: 31,
        3: 53,
        4: 75,
        5: 102,
    },
    "Rings": {
        "Damage": {
            0: 0,
            1: 25,
            2: 50,
            3: 100,
        },
        "Armor": {
            0: 0,
            1: 20,
            2: 40,
            3: 80,
        },
    },
}

with open(file_name, "r") as file:
    BOSS = {}
    for line in file:
        stat, value = line.split(": ")
        BOSS[stat] = int(value)

HIT_POINTS_BOSS = BOSS["Hit Points"]
DAMAGE_BOSS = BOSS["Damage"]
ARMOR_BOSS = BOSS["Armor"]
HIT_POINTS_PLAYER = 8 if EXAMPLE else 100

if EXAMPLE:
    pprint(BOSS, sort_dicts=False)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def shopping(reverse=False):
    return sorted(
        ((d + dd, a + ad, cost_d + cost_dd + cost_a + cost_ad)
         for d, cost_d in SHOP["Damage"].items()
         for dd, cost_dd in SHOP["Rings"]["Damage"].items()
         for a, cost_a in SHOP["Armor"].items()
         for ad, cost_ad in SHOP["Rings"]["Armor"].items()),
        key=lambda t: t[2],
        reverse=reverse
    )


def fight(player):    
    damage_player = max(1, player["Damage"] - ARMOR_BOSS)
    n_player, r = divmod(HIT_POINTS_BOSS, damage_player)
    n_player += 0 if r == 0 else 1

    damage_boss = max(1, DAMAGE_BOSS - player["Armor"])
    n_boss, r = divmod(HIT_POINTS_PLAYER, damage_boss)
    n_boss += 0 if r == 0 else 1
    
    return "PLAYER" if n_player <= n_boss else "BOSS"

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    for damage, armor, costs in shopping():
        player = {"Damage": damage, "Armor": armor}
        if fight(player) == "PLAYER":
            return costs


solution = part_1()
assert solution == (65 if EXAMPLE else 121)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    for damage, armor, costs in shopping(reverse=True):
        player = {"Damage": damage, "Armor": armor}
        if fight(player) == "BOSS":
            return costs


solution = part_2()
assert solution == (188 if EXAMPLE else 201)
print(solution)
