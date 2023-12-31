# --------------------------------------------------------------------------- #
#    Day 2                                                                   #
# --------------------------------------------------------------------------- #

DAY = 2
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    strategy = [line.strip().split() for line in file]
#print(strategy)

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

SHAPES = {
    "A": "Rock", "B": "Paper", "C": "Scissors",
    "X": "Rock", "Y": "Paper", "Z": "Scissors"
}
SCORES = {"Rock": 1, "Paper": 2, "Scissors": 3}
LOSES = {("Rock", "Scissors"), ("Scissors", "Paper"), ("Paper", "Rock")}
WINS = set((b, a) for a, b in LOSES)


def score(a, b):
    a, b = SHAPES[a], SHAPES[b]
    score = SCORES[b]
    if a == b:
        return score + 3
    if (a, b) in WINS:
        return score + 6
    return score

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

print(sum(score(a, b) for a, b in strategy))

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

LOSES = dict(LOSES)
WINS = dict(WINS)


def score(a, b):
    a = SHAPES[a]
    if b == "X":
        return SCORES[LOSES[a]]
    if b == "Y":
        return SCORES[a] + 3
    return SCORES[WINS[a]] + 6
        
print(sum(score(a, b) for a, b in strategy))
