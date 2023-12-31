# --------------------------------------------------------------------------- #
#    Day 4                                                                    #
# --------------------------------------------------------------------------- #

DAY = 4
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

cards = []
with open(file_name, "r") as file:
    for line in file:
        winning, games = line.split(": ")[1].split(" | ")
        winning = set(map(int, winning.strip().split()))
        games = list(map(int, games.strip().split()))
        cards.append((winning, games))

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    points = 0
    for winning, games in cards:
        num_wins = sum(1 for card in games if card in winning)
        if num_wins > 0:
            points += 2 ** (num_wins - 1)
    return points


solution = part_1()
assert solution == (13 if EXAMPLE else 26346)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    card_counts = dict.fromkeys(range(len(cards)), 1)
    total_count = 0
    for card, (winning, games) in enumerate(cards):
        total_count += (copies := card_counts[card])
        for game_card in games:
            if game_card in winning:
                card_counts[card := card + 1] += copies                
    return total_count


solution = part_2()
assert solution == (30 if EXAMPLE else 8467762)
print(solution)
