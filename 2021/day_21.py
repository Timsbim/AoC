# --------------------------------------------------------------------------- #
#    Day 21                                                                   #
# --------------------------------------------------------------------------- #
from collections import Counter, defaultdict
from itertools import cycle
from pprint import pprint


DAY = 21
EXAMPLE = True

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
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #


def next_position(position, score):
    return (position + score) % 10 or 10


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
        for i in range(2):
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
print("Part 2: ", end="\n\n")

DIST = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}



def get_steps(start):
    steps = []
    last_step = {start: {0: 1}}
    while True:
        step = defaultdict(Counter)
        for start in last_step:
            for roll in 1, 2, 3:
                position = score = next_position(start, roll)
                for score_old, num in last_step[start].items():
                    if score_old < 21:
                        if (score_new := score_old + score) > 21:
                            score_new = 21
                        step[position][score_new] += num
        steps.append(sum(step.values(), Counter()))
        if len(steps[-1]) == 1:
            break
        last_step = step
    return steps



"""
for start in 4, 8:
    steps = get_steps(start)
    print(f"Start: {start}")
    for n, step in enumerate(steps, start=1):
        print(f"Step {n}: ", end="")
        print({s: step[s] for s in sorted(step)})

steps = get_steps(8)
for n, step in enumerate(steps, 1):
    non_wins = sum(n for s, n in step.items() if s < 21)
    print(f"Step {n}: {step[21]}, {non_wins}")

"""


"""
step_max = 8
step = wins_0 = wins_1 = 0
paths = [((0, 4), (0, 8))]
while paths:
    step += 1
    next_paths = []
    for (s0, p0), (s1, p1) in paths:
        for roll in 1, 2, 3:
            if step % 2 == 1:  # Player 1's turn
                p0_next = next_position(p0, roll)
                s0_next = s0 + p0_next
                if s0_next >= 21:
                    wins_0 += 1
                else:
                    next_paths.append(((s0_next, p0_next), (s1, p1)))
            else:  # Player 2's turn
                p1_next = next_position(p1, roll)
                s1_next = s1 + p1_next
                if s1_next >= 21:
                    wins_1 += 1
                else:
                    next_paths.append(((s0, p0), (s1_next, p1_next)))
    paths = next_paths
    print(f"Step {step}: {len(paths)} open paths")

print(f"\n1 wins: {wins_0}; 2 wins: {wins_1}\n")
# 444356092776315
# 341960390180808 
"""