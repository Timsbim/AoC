# --------------------------------------------------------------------------- #
#    Day 22                                                                   #
# --------------------------------------------------------------------------- #
from collections import namedtuple
from pprint import pprint


DAY = 22
EXAMPLE = True

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

with open(file_name, "r") as file:
    BOSS = {}
    for line in file:
        stat, value = line.split(": ")
        BOSS[stat] = int(value)
    
PLAYER = (
    {"Hit Points": 14, "Mana": 250}
    if EXAMPLE else
    {"Hit Points": 50, "Mana": 500}
)

print(f"Boss: {BOSS}; Player: {PLAYER}")

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

Spell = namedtuple(
    "Spell",
    "Cost Cooldown Damage Armor Heal Mana".split(),
    defaults=(0, 0, 0, 0, 0)
)

spell = Spell(10)

SPELLS = {
    "Missile":  Spell(53, Damage=4),
    "Drain":    Spell(73, Damage=2, Heal=2),
    "Shield":   Spell(113, Cooldown=6, Armor=7),
    "Poison":   Spell(173, Cooldown=6, Damage=3),
    "Recharge": Spell(229, Cooldown=5, Mana=101)
}
pprint(SPELLS, sort_dicts=False)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    """Ojective: find the least amount of mana spent to win over the boss"""
    return None


solution = part_1()
# assert solution == (if EXAMPLE else)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return None


solution = part_2()
# assert solution == (if EXAMPLE else)
print(solution)
