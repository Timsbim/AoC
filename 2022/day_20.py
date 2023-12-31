# --------------------------------------------------------------------------- #
#    Day 20                                                                   #
# --------------------------------------------------------------------------- #

DAY = 20
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
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

def get_numbers(file_name):
    with open(file_name, "r") as file:
        return list(map(int, file))

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def print_shifts(length, old, file=None):
    """ Prints the movements of index old through one cycle of shifts (+ and -).
    E.g. for length = 5 and old = 3:

        +----------------------+
        |0 1 2 3 4|  |0 1 2 3 4|
        |---------|  |---------|
        |0 1 2 4 3|  |0 1 3 2 4|
        |0 3 1 2 4|  |0 3 1 2 4|
        |0 1 3 2 4|  |0 1 2 4 3|
        |0 1 2 3 4|  |0 1 2 3 4|
        +----------------------+
    """
    numbers = list(range(length))
    
    # Forward shifts
    rows = [" ".join(map(str, numbers)), "-" * (2 * length - 1)]
    for shift in range(1, length):
        new = 1 + (old - 1 + shift) % (length - 1)
        shifted = move(numbers, old, new)
        rows.append(" ".join(map(str, shifted)))
    rows.append(" ".join(map(str, numbers)))

    # Backward shifts
    rows.extend((" ".join(map(str, numbers)), "-" * (2 * length - 1)))
    for shift in range(1, length):
        shift = (-shift) % (length - 1)
        new = 1 + (old - 1 + shift) % (length - 1)
        shifted = move(numbers, old, new)
        rows.append(" ".join(map(str, shifted)))

    # Formatting and output
    rows = ["+" + "-" * (4 * length + 2) + "+"] + [
        f"|{left}|  |{right}|" for left, right in zip(rows, rows[length + 2:])
    ] + ["+" + "-" * (4 * length + 2) + "+"]
    string = "\n".join(rows)
    print(string)
    if file is not None:
        with open("output.txt", "w") as file:
            file.write(string)


def move(mixed, old, new):
    if old == new:
        return mixed
    if old < new:
        return (
            mixed[:old]               # Part before the moving item
            + mixed[old + 1:new + 1]  # Part between old and new position
            + [mixed[old]]            # Moved item
            + mixed[new + 1:]         # Rest after new position
        )
    return (
        mixed[:new]                  # Part before the new position
        + [mixed[old]]               # Moved item
        + mixed[new:old]             # Part beween new and old position
        + mixed[old + 1:]            # Rest after old position
    )    


def new_index(length, old, shift):
    # Nothing to do
    if shift == 0:
        return old
    # Reduce number of shifts to rest modulo length - 1 (size of the cycle)
    shift %= (length - 1)
    # New position always beyond index 0: Add shift to normalized start index
    # old, and then reduce the result to the rest module cycle length.
    return 1 + (old - 1 + shift) % (length - 1)


def coordinates(mixed):
    idx_0 = mixed.index(0)
    indices = ((idx_0 + n * 1_000) % len(mixed) for n in range(1, 4))
    return tuple(mixed[i] for i in indices)
    
# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def mixing(numbers):
    length = len(numbers)
    mixed = list(range(length))
    for i, shift in enumerate(numbers):
        old = mixed.index(i)
        new = new_index(length, old, shift)
        mixed = move(mixed, old, new)
    return [numbers[i] for i in mixed]


mixed = mixing(get_numbers(file_name))
print(sum(coordinates(mixed)))  # 4578
 
# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def mixing(numbers):
    decryption_key = 811589153
    numbers = [number * decryption_key for number in numbers]
    order = [(i, number) for i, number in enumerate(numbers)]
    length = len(numbers)
    mixed = list(range(length))
    for _ in range(10):
        for i, shift in order:
            old = mixed.index(i)
            new = new_index(length, old, shift)
            mixed = move(mixed, old, new)
    return [numbers[i] for i in mixed]


mixed = mixing(get_numbers(file_name))
print(sum(coordinates(mixed)))  # 2159638736133
