# --------------------------------------------------------------------------- #
#    Day 24                                                                   #
# --------------------------------------------------------------------------- #

from pprint import pprint
from operator import add, mul, floordiv, mod, eq
from itertools import product
from random import choices

DAY = 24
EXAMPLE = True

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2021/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    code = [tuple(line.strip().split()) for line in file]

# pprint(code)

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

OPERATORS = {"add": add, "mul": mul, "div": floordiv, "mod": mod, "eql": eq}


def operation(state, instruction, model_number):
    op, *arguments = instruction
    if op == "inp":
        state[arguments[0]] = int(model_number.pop())
        return
    argument_1, argument_2 = arguments
    number_1 = state[argument_1]
    if argument_2.startswith("-") or argument_2.isdigit():
        number_2 = int(argument_2)
    else:
        number_2 = state[argument_2]
    state[argument_1] = OPERATORS[op](number_1, number_2)


def run_monad(code, model_number):
    model_number = list(reversed(model_number))
    state = {"w": 0, "x": 0, "y": 0, "z": 0}
    for instruction in code:
        operation(state, instruction, model_number)
    return not bool(state["z"])


def create_mondad(code):
    operators = {"add": "+", "mul": "*", "div": "//", "mod": "%"}
    indent = "    "
    with open("day_24_monad.py", "w") as file:
        file.write("def run_monad(model_number):\n")
        file.write(indent + "w = x = y = z = 0\n")
        inp_count = 0
        for op, *arguments in code:
            if op == "inp":
                file.write(
                    indent
                    +  f"{arguments[0]} = int(model_number[{str(inp_count)}])\n"
                )
                inp_count += 1
            else:
                arg_1, arg_2 = arguments
                if op == "eql":
                    file.write(indent + f"{arg_1} = ({arg_1} == {arg_2})\n")
                else:
                    file.write(indent + f"{arg_1} {operators[op]}= {arg_2}\n")
        file.write(indent + "return z")


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

create_mondad(code)

from day_24_monad import run_monad
from day_24_monad_reduced import run_monad_reduced

digits = "987654321"
for _ in range(100_000):
    number = "".join(choices(digits, k=14))
    if not run_monad(number) == run_monad_reduced(number):
        print(f"Difference for number: {number} :(")
        with open("difference.txt", "w") as file:
            file.write(number)
        break
else:
    print("All good :)")

"""
    Implications:

    w_4 = w_3 - 1
    w_5 == w_2 - 4
    w_6 == 1
    w_7 == 9
    w_9 == w_8 + 4
    w_11 == w_10 + 3
    w_12 == w_1 + 1
    w_13 == w_0 - 2

    -> 9899 8519 5969 97
"""

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

"""
    Implications:
    
    w_4 = w_3 - 1
    w_5 == w_2 - 4
    w_6 == 1
    w_7 == 9
    w_9 == w_8 + 4
    w_11 == w_10 + 3
    w_12 == w_1 + 1
    w_13 == w_0 - 2

    -> 3152 1119 1514 21
"""


"""
def run_monad_reduced(model_number):
    w = x = y = z = 0
    
    w_0 = int(model_number[0])
    z_0 = (w_0 + 10)
    
    w_1 = int(model_number[1])
    z_1 = z_0 * 26 + (w_1 + 16)
    
    w_2 = int(model_number[2])
    z_2 = z_1 * 26 + (w_2 + 0)
    
    w_3 = int(model_number[3])
    z_3 = z_2 * 26 + (w_3 + 13)
    
    w_4 = int(model_number[4])
    x = z_3 % 26 - 14
    x = 0 if x == w_4 else 1
    z_3 = z_2 
    z_4 = z_3 * (25 * x + 1) + x * (w_4 + 7)

    w_5 = int(model_number[5])
    x = z_4 % 26 - 4
    x = 0 if x == w_5 else 1
    z_4 //= 26  # z_4 == z_1
    z_5 = z_4 * (25 * x + 1) + x * (w_5 + 11)
    
    w_6 = int(model_number[6])
    z_6 = z_5 * 26 + (w_6 + 11)
    
    w_7 = int(model_number[7])
    x = z_6 % 26 - 3
    x = 0 if x == w_7 else 1
    z_6 = z_5  # z_6 == z_1
    z_7 = z_6 * (25 * x + 1) + x * (w_7 + 10)
    
    w_8 = int(model_number[8])
    z_8 = z_7 * 26 + (w_8 + 16)
    
    w_9 = int(model_number[9])
    x = z_8 % 26 - 12
    x = 0 if x == w_9 else 1
    z_8 = z_7  # z_8 == z_1
    z_9 = z_8 * (25 * x + 1) + x * (w_9 + 8)
    
    w_10 = int(model_number[10])
    z_10 = z_9 * 26 + (w_10 + 15)
    
    w_11 = int(model_number[11])
    x = z_10 % 26 - 12
    x = 0 if x == w_11 else 1
    z_10 = z_9  # z_10 == z_1
    z_11 = z_10 * (25 * x + 1) + x * (w_11 + 2)
    
    w_12 = int(model_number[12])
    x = z_11 % 26 - 15
    x = 0 if x == w_12 else 1
    z_11 //= 26  # z_11 = z_0
    z_12 = z_11 * (25 * x + 1) + x * (w_12 + 5)
    
    w_13 = int(model_number[13])
    x = z_12 % 26 - 12
    x = 0 if x == w_13 else 1
    z_12 //= 26  # z_12 == 0
    z_13 = z_12 * (25 * x + 1) + x * (w_13 + 10)
    
    return z_13
"""
