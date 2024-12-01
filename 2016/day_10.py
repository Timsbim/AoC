# --------------------------------------------------------------------------- #
#    Day 10                                                                   #
# --------------------------------------------------------------------------- #
from collections import defaultdict
from pprint import pprint


DAY = 10
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2016/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #


def new_bot():
    return {"low": None, "low_to": None, "high": None, "high_to": None}


def read_input(file_name):
    # Read the input into bots and output bins
    bots = {}
    with open(file_name, "r") as file:
        for line in file:
            row = line.split()
            if row[0] == "value":
                value = int(row[1])
                bot = bots.setdefault(int(row[-1]), new_bot())
                if bot["low"] is None:
                    bot["low"] = value
                else:
                    value_low = bot["low"]
                    bot["low"] = min(value_low, value)
                    bot["high"] = max(value_low, value)
            else:
                bot = bots.setdefault(int(row[1]), new_bot())
                bot["low_to"] = row[5], int(row[6])
                bot["high_to"] = row[-2], int(row[-1])
    
    # Find starting point
    starts = [
        no
        for no, bot in bots.items()
        if bot["high"] is not None and bot["low"] is not None
    ]
    assert len(starts) == 1  # Check if starting point is unique
    
    return starts[0], bots, defaultdict(list)


if EXAMPLE:
    start, bots, outs = read_input(file_name)
    print(f"Starting bot: {start}")
    print("Bots:")
    pprint(bots)
    print("Output bins:")
    pprint(outs)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def bot_step(v1, bot):
    low, high = bot["low"], bot["high"]
    if low is None and high is None:
        bot["low"] = v1
    else:
        v2 = high if low is None else low
        bot["low"], bot["high"] = (v1, v2) if v1 <= v2 else (v2, v1)
        return bot


def process(file_name):
    start, bots, outs = read_input(file_name)
    comps, stack = [], [start]
    while stack:
        stack_new = []
        for no in stack:
            bot = bots[no]
            comps.append((no, bot["low"], bot["high"]))
            for kind in "low", "high":
                value, (to, no) = bot[kind], bot[f"{kind}_to"]
                bot[kind] = None
                if to == "output":
                    outs[no].append(value)
                else:
                    if bot_step(value, bots[no]) is not None:
                        stack_new.append(no)                
        stack = stack_new
    return outs, comps


outs, comps = process(file_name)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

LOW, HIGH = (2, 5) if EXAMPLE else (17, 61)


def part_1(comps):
    for no, low, high in comps:
        if low == LOW and high == HIGH:
            return no


print(solution := part_1(comps))
assert solution == (2 if EXAMPLE else 86)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(outs):
    return outs[0][0] * outs[1][0] * outs[2][0]


print(solution := part_2(outs))
assert solution == (30 if EXAMPLE else 22847)
