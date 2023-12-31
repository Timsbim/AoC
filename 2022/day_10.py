# --------------------------------------------------------------------------- #
#    Day 10                                                                   #
# --------------------------------------------------------------------------- #

DAY = 10
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def commands(file_name):
    with open(file_name, "r") as file:
        for line in file:
            yield "noop", None
            if line.startswith("addx"):
                yield "addx", int(line[line.rfind(" "):])
    
# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def sum_signal_strength(commands):
    checkpoints = {20, 60, 100, 140, 180, 220}
    x, strength = 1, 0
    for cycle, (cmd, arg) in enumerate(commands, 1):
        if cycle in checkpoints:
            strength += cycle * x
        if cmd == "addx":
            x += arg
    return strength


print(sum_signal_strength(commands(file_name)))  # 12880
            
# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2:")


def crt(commands):
    image, x, sprite = [], 1, range(3)
    for cycle, (cmd, arg) in enumerate(commands):
        idx = cycle % 40
        if idx == 0:
            row = [" "] * 40
        if idx in sprite:
            row[idx] = "#"
        if cmd == "addx":
            x += arg
            sprite = range(x - 1, x + 2)
        if idx == 39:
            image.append("".join(row))
    return "\n".join(image)


print(crt(commands(file_name))) # FCJAPJRE
