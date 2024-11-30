# --------------------------------------------------------------------------- #
#    Day 21                                                                   #
# --------------------------------------------------------------------------- #

from operator import add, sub, mul, floordiv, eq

DAY = 21
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2022/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

OPERATORS = {"+": add, "-": sub, "*": mul, "/": floordiv}


def get_monkeys(file_name):
    numbers, mathers = {}, {}
    with open(file_name, "r") as file:
        for line in file:
            left, right = line.strip().split(": ")
            if right.isdigit():
                numbers[left] = int(right)
            else:
                arg1, op, arg2 = right.split()
                mathers[left] = {0: arg1, 1: arg2, "op": OPERATORS[op]}
    return numbers, mathers

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def listen_to_root(numbers, mathers):
    numbers = dict(numbers)
    go = True
    used = set()
    while go:
        for monkey in list(mathers.keys() - used):
            func = mathers[monkey]
            left, right, op = func[0], func[1], func["op"]
            if left in numbers and right in numbers:
                number = op(numbers[left], numbers[right])
                if monkey == "root":
                    return number
                numbers[monkey] = number
                used.add(monkey)


numbers, mathers = get_monkeys(file_name)
print(listen_to_root(numbers, mathers))  # 169525884255464
                
# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="\n")


def get_ordered_monkeys(numbers, mathers):
    used = []
    input_monkeys = ["root"]
    while input_monkeys:
        used += input_monkeys
        next_input_monkeys = []
        for monkey in input_monkeys:
            func = mathers[monkey]
            left, right = func[0], func[1]
            if left not in numbers:
                next_input_monkeys.append(left)
            if right not in numbers:
                next_input_monkeys.append(right)
        input_monkeys = next_input_monkeys
    return list(reversed(used))


def descendents(numbers, mathers, root="humn"):
    descendents = set()
    next_shift = [root]
    while next_shift:
        new_next_shift = []
        for number in next_shift:
            for monkey in mathers:
                func = mathers[monkey]
                if number == func[0] or number == func[1]:
                    descendents.add(monkey)
                    new_next_shift.append(monkey)
        next_shift = new_next_shift
    return descendents


def calculate_numbers(numbers, mather):
    numbers = dict(numbers)
    monkeys = get_ordered_monkeys(numbers, mathers)
    for monkey in monkeys:
        func = mathers[monkey]
        left, right, op = func.values()
        numbers[monkey] = op(numbers[left], numbers[right])
    return numbers


def optimize_monkeys(numbers, mathers):
    humn_descendents = descendents(numbers, mathers)
    numbers = {
        monkey: number
        for monkey, number in calculate_numbers(numbers, mathers).items()
        if monkey not in humn_descendents
    }
    mathers = {monkey: mathers[monkey] for monkey in humn_descendents}
    return numbers, mathers


def when_is_root_true(
    numbers, mathers, max_n=5_000, file_name="output.txt"
):
    base_numbers, mathers = optimize_monkeys(numbers, mathers)
    mathers["root"]["op"] = eq
    monkeys = [
        (monkey,) + tuple(mathers[monkey].values())
        for monkey in get_ordered_monkeys(base_numbers, mathers)
    ]
    del base_numbers["humn"]
    root, root_left, root_right, _ = monkeys[-1]
    with open(file_name, "w") as file:
        n = -1
        while True:
            n += 1
            numbers = dict(base_numbers)
            numbers["humn"] = n
            for monkey, left, right, op in monkeys:
                numbers[monkey] = op(numbers[left], numbers[right])
            string = f"{numbers[root_left]:_},{numbers[root_right]:_}"
            print(string, file=file)
            if n == max_n:
                break


"""
RESULT: 3247317268284

STRATEGY:

(1) Output the arguments for root for some 1,000 inputs: 0, 1, 2, ... 
(2) Generate the diffs.
(3) Look for periodicity p (63).
(4) Divide the difference between the first and second root-argument by
    the sum over one diff-period -> m (51_544_718_544). Take the rest and
    and check how many diffs it takes to cover the rest -> n (12).
(5) Result = p * m + n (3_247_317_268_284).
"""
