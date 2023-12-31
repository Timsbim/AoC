 # --------------------------------------------------------------------------- #
#    Day 9                                                                    #
# --------------------------------------------------------------------------- #

DAY = 9
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

def instructions(file_name):
    with open(file_name, "r") as file:
        for line in file:
            direction, count = line.rstrip().split()
            yield from (direction for _ in range(int(count)))


def move(head, instruction):
    if instruction == "R":
        head[0] += 1
    elif instruction == "U":
        head[1] += 1
    elif instruction == "L":
        head[0] -= 1
    elif instruction == "D":
        head[1] -= 1
    

def follow(head, tail):
    delta = head[0] - tail[0], head[1] - tail[1]
    delta_abs = abs(delta[0]), abs(delta[1])
    if max(delta_abs) > 1:
        for i in 0, 1:
            if delta[i] != 0:
                tail[i] += delta[i] // delta_abs[i]

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

tail_trail = {(0, 0)}
head, tail = [0, 0], [0, 0]
for instruction in instructions(file_name):
    move(head, instruction)
    follow(head, tail)
    tail_trail.add(tuple(tail))

print(len(tail_trail))  # 5883

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

tail_trail = {(0, 0)}
bridge = [[0, 0] for _ in range(10)]
for instruction in instructions(file_name):
    move(bridge[0], instruction)
    for head, tail in zip(bridge, bridge[1:]):
        follow(head, tail)
    tail_trail.add(tuple(bridge[-1]))

print(len(tail_trail))  # 2367
