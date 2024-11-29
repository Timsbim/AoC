# --------------------------------------------------------------------------- #
#    Day 22                                                                   #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 22
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #
 
BOSS_HP, DAMAGE, PLAYER_HP, MANA = (
    (14, 8, 14, 250) if EXAMPLE else (58, 9, 50, 500)
)
 
# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #
 
SPELLS_DIRECT = ("Missile", 53), ("Drain", 73)
SPELLS_DELAYED = ("Shield", 113, 6), ("Poison", 173, 6), ("Recharge", 229, 5)
 

def fights(hard=False):
    minimum = float("inf")
    
    stack = [(0, BOSS_HP, PLAYER_HP, MANA, 0, tuple())]
    while stack:  # DFS
        turn, boss_hp, player_hp, mana, costs, spells = stack.pop()
       
        # Discontinue the branch if costs are too high
        if costs >= minimum:
            continue

        # Hard mode
        if hard and turn % 2 == 0:
            player_hp -= 1
            if player_hp <= 0:
                continue
        
        # Effects at the beginning of the turn
        armor = 0
        spells_new, spells_active = [], set()
        for spell, cooldown in spells:
            match spell:  # Effects
                case "Shield": armor = 7
                case "Poison": boss_hp -= 3
                case "Recharge": mana += 101
            if cooldown > 1:  # Cooldown reduction
                spells_new.append((spell, cooldown - 1))
                spells_active.add(spell)
        if boss_hp <= 0:  # Adjust minimum if boss is dead
            minimum = min(minimum, costs)
            continue
        spells_new = tuple(spells_new)
        
        if (turn := turn + 1) % 2:  # Players turn           
            # Choose next spell
            for spell, cost in SPELLS_DIRECT:  # Spells with direct results
                costs_new = costs + cost
                if cost > mana or costs_new >= minimum:  # Not enough mana or suboptimal
                    break
                boss_hp_new, player_hp_new = boss_hp, player_hp
                match spell:
                    case "Missile": boss_hp_new -= 4
                    case "Drain":
                        boss_hp_new -= 2
                        player_hp_new += 2
                if boss_hp_new <= 0:  # Adjust minimum if boss is dead
                    minimum = min(minimum, costs_new)
                else:
                    stack.append((
                        turn, boss_hp_new, player_hp_new,
                        mana - cost, costs_new,
                        spells_new
                    ))
 
            for spell, cost, cooldown in SPELLS_DELAYED:  # Spells with delayed results
                costs_new = costs + cost
                if cost > mana or costs_new >= minimum:  # Not enough mana or suboptimal
                    break
                if spell not in spells_active:
                    stack.append((
                        turn, boss_hp, player_hp, mana - cost, costs_new,
                        spells_new + ((spell, cooldown),)
                    ))

        else:  # Bosses turn
            # Damage
            player_hp -= max(1, DAMAGE - armor)
 
            # Extend stack if player still alive
            if player_hp > 0:
                stack.append((
                    turn, boss_hp, player_hp, mana, costs, spells_new
                ))
   
    return minimum
 

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")
 

def part_1():
    return fights()


print(solution := part_1())
assert solution == (568 if EXAMPLE else 1269)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    return fights(hard=True)


print(solution := part_2())
assert solution == (float("inf") if EXAMPLE else 1309)
