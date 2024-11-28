# --------------------------------------------------------------------------- #
#    Day 21                                                                   #
# --------------------------------------------------------------------------- #
from collections import Counter, defaultdict
from itertools import cycle


DAY = 21
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2021/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    start_1 = int(next(file).strip()[-1])
    start_2 = int(next(file).strip()[-1])
print("Input:", start_1, start_2)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")
 

def deterministic_rolls():
    dice = cycle(range(1, 101))
    while True:
        yield next(dice) + next(dice) + next(dice)


def part_1(start_1, start_2):
    die = deterministic_rolls()
    position, score, counter = [start_1, start_2], [0, 0], 0
    while True:
        for i in 0, 1:
            position[i] = (position[i] + next(die)) % 10 or 10
            counter += 3
            score[i] += position[i]
            if score[i] >= 1000:
                i = (i + 1) % 2
                return score[i] * counter


solution = part_1(start_1, start_2)
assert solution == (739785 if EXAMPLE else 513936)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

# Rolls distribution: 3 independent rolls with result 1, 2 or 3
ROLLS = (3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)
 

def get_states(start):
    """Calculate the finishing leafs and pending branches over the (simplified)
    turn tree
    """
    states = []
    turn_last = {start: {0: 1}}
    while True:
        turn = defaultdict(Counter)
        for start in turn_last:
            for rolls, n in ROLLS:
                position = (start + rolls) % 10 or 10
                for score, m in turn_last[start].items():
                    if score >= 21: continue
                    turn[position][min(score + position, 21)] += n * m    
        turn_last = turn
        scores = sum(turn.values(), Counter())
        states.append((scores[21], sum(scores.values()) - scores[21]))
        if len(scores) == 1:
            return states
 

def part_2(start_1, start_2):
    """Use the finishing/pending states of the 2 players to count the wins:
    sum over #(finishing branches) x #(pending branches) of other player one
    turn before
    """
    pending_2 = wins_1 = wins_2 = 0
    states = zip(get_states(start_1), get_states(start_2))
    for (finishing_1, pending_1), (finishing_2, pending_2_new) in states:
        wins_1 += finishing_1 * pending_2
        wins_2 += finishing_2 * pending_1
        pending_2 = pending_2_new
    return max(wins_1, wins_2)
 

solution = part_2(start_1, start_2)
print(solution)
assert solution == (444356092776315 if EXAMPLE else 105619718613031)
