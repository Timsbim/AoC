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

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

BOSS = (
    {"Hit Points": 14, "Damage": 8}
    if EXAMPLE else
    {"Hit Points": 58, "Damage": 9}
)   
PLAYER = (
    {"Hit Points": 14, "Mana": 250}
    if EXAMPLE else
    {"Hit Points": 50, "Mana": 500}
)

print(f"Player: {PLAYER}; Boss: {BOSS}\n")

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

Spell = namedtuple(
    "Spell",
    "Cost Cooldown Damage Armor Heal Mana".split(),
    defaults=(0, 0, 0, 0, 0)
)

SPELLS = {
    "Missile":  Spell(53, Damage=4),
    "Drain":    Spell(73, Damage=2, Heal=2),
    "Shield":   Spell(113, Cooldown=6, Armor=7),
    "Poison":   Spell(173, Cooldown=6, Damage=3),
    "Recharge": Spell(229, Cooldown=5, Mana=101)
}
pprint(SPELLS, sort_dicts=False)

SPELLS = (
    Spell(53, Damage=4),
    Spell(73, Damage=2, Heal=2),
    Spell(113, Cooldown=6, Armor=7),
    Spell(173, Cooldown=6, Damage=3),
    Spell(229, Cooldown=5, Mana=101)
)
pprint(SPELLS)
cooldowns = {spell: spell.Cooldown for spell in SPELLS}
pprint(cooldowns)


SPELLS = tuple("Missile Drain Shield Poison Recharge".split())
COSTS = (53, 73, 113, 173, 229)


def effects(state):
    hp_boss, hp_player, mana, cooldowns = state

    new_cooldowns = []
    for spell, cooldown in zip(SPELLS[2:], cooldowns):
        new_cooldowns.append(cooldown - 1 if cooldown > 0 else 0)
        if cooldown > 0:
            if spell == "Shield":
                armor = 7
            elif spell == "Poison":
                hp_boss -= 3
            elif spell == "Recharge":
                mana += 101
    
    return hp_boss, hp_player, mana, tuple(new_cooldowns)


def fights():
    minimum = float("inf")
    
    hp_boss, damage = BOSS["Hit Points"], BOSS["Damage"]
    hp_player, mana = PLAYER["Hit Points"], PLAYER["Mana"]
    paths = [(0, hp_boss, hp_player, mana, (0, 0, 0))]
    while paths:
        path = paths.pop()
        costs, state = path[0], path[1:]
        
        # Players turn
        hp_boss, hp_player, mana, cooldowns = effects(state)
        if hp_boss <= 0:
            minimum = min(minimum, costs)
            continue
        if mana < 53:
            continue

        for spell, cost in zip(SPELLS, COSTS):
            if cost <= mana:
                
        
        # Bosses turn
        hp_player -= max(1, armor - damage)

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
