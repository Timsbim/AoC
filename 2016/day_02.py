# --------------------------------------------------------------------------- #
#    Day 2                                                                    #
# --------------------------------------------------------------------------- #
from pprint import pprint


DAY = 2
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2016/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    directions = tuple(file.read().splitlines())
if EXAMPLE:
    pprint(directions)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #


def solve(pad, move, directions, start):
    position, chars = start, []
    for direction in directions:
        for instruction in direction:
            position = move(position, instruction)
        chars.append(pad[position])
    return "".join(chars)


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(directions):
    PAD = {
        (0, 2): '1', (1, 2): '2', (2, 2): '3',
        (0, 1): '4', (1, 1): '5', (2, 1): '6',
        (0, 0): '7', (1, 0): '8', (2, 0): '9'
    }
    
    
    def move(position, instruction):
        x, y = position
        if instruction == 'U':
            return x, min(2, y + 1)
        if instruction == 'D':
            return x, max(0, y - 1)
        if instruction == 'R':
            return min(2, x + 1), y
        return max(0, x - 1), y

    
    return solve(PAD, move, directions, (1, 1))


print(solution := part_1(directions))
assert solution == ("1985" if EXAMPLE else "14894")

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(directions):
    PAD = {
        ( 0,  2): '1',
        (-1,  1): '2', ( 0,  1): '3', (1,  1): '4',
        (-2,  0): '5', (-1,  0): '6', (0,  0): '7', (1, 0): '8', (2, 0): '9',
        (-1, -1): 'A', ( 0, -1): 'B', (1, -1): 'C',
        ( 0, -2): 'D'
    }
    
    
    def move(position, instruction):
        x, y = position
        if instruction == 'U':
            position_new = x, y + 1
        elif instruction == 'D':
            position_new = x, y - 1
        elif instruction == 'R':
            position_new = x + 1, y
        else:
            position_new = x - 1, y
        return position_new if position_new in PAD else position

    
    return solve(PAD, move, directions, (-2, 0))


print(solution := part_2(directions))
assert solution == ("5DB3" if EXAMPLE else "26B96")
