# --------------------------------------------------------------------------- #
#    Day 19                                                                   #
# --------------------------------------------------------------------------- #
import re
import sys

from pprint import pprint


DAY = 19
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2015/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    lines = file.read().splitlines()
MEDICINE = lines[-1]
MAPPING = {}
for line in lines[:-2]:
    left, right = line.split(" => ")
    MAPPING.setdefault(left, set()).add(right)

if EXAMPLE:
    print(MEDICINE)
    pprint(MAPPING)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    return len({
        MEDICINE[:m.start()] + ma + MEDICINE[m.end():]
        for a, ms in MAPPING.items()
        for ma in ms
        for m in re.finditer(a if len(a) == 2 else f"{a}(?![a-z])", MEDICINE)
    })


solution = part_1()
assert solution == (4 if EXAMPLE else 576)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

if EXAMPLE:
    # Since the first replacement results in atom count 1 and every
    # replacement afterwords increases the atom count by 1
    print(len(HOH))
    sys.exit()


# Transform medicine and targets in MAPPING in tuple of atoms

re_atom = re.compile(r"[A-Z][a-z]|[A-Z]")
medicine = tuple(re_atom.findall(MEDICINE))
mapping = {
    a: [tuple(re_atom.findall(m)) for m in ms]
    for a, ms in MAPPING.items()
}

# Check for atoms in target molecules that can't be mapped ("unchangeables"):
#     => Y, Rn, Ar, C

unchangeables = set().union(*(set().union(*ms) for ms in mapping.values()))
unchangeables -= mapping.keys()

# Check if there are unchangables that are not in the medicine: C
#    => Target molecules that contain C are irrelevant

excludes = unchangeables - set(medicine)

# Afterwards remove those target molecules to simplify the graph

mapping = {
    a: [m for m in ms if excludes.isdisjoint(m)]
    for a, ms in mapping.items()
}

#  Reduced mapping:
#
#  {'Al': [('Th', 'F'), ('Th', 'Rn', 'F', 'Ar')],
#   'B':  [('Ti', 'Rn', 'F', 'Ar'), ('B', 'Ca'), ('Ti', 'B')],
#   'Ca': [('Si', 'Th'), ('P', 'B'), ('Si', 'Rn', 'F', 'Y', 'F', 'Ar'),
#          ('P', 'Rn', 'F', 'Ar'), ('Si', 'Rn', 'Mg', 'Ar'), ('Ca', 'Ca')],
#   'F':  [('Ca', 'F'), ('P', 'Mg'), ('Si', 'Al')],
#   'H':  [('H', 'Ca'), ('N', 'Th'), ('O', 'Rn', 'F', 'Ar'),
#          ('N', 'Rn', 'F', 'Y', 'F', 'Ar'), ('O', 'B'),
#          ('N', 'Rn', 'Mg', 'Ar')],
#   'Mg': [('Ti', 'Mg'), ('B', 'F')],
#   'N':  [('H', 'Si')],
#   'O':  [('O', 'Ti'), ('N', 'Rn', 'F', 'Ar'), ('H', 'P')],
#   'P':  [('Si', 'Rn', 'F', 'Ar'), ('Ca', 'P'), ('P', 'Ti')],
#   'Si': [('Ca', 'Si')],
#   'Th': [('Th', 'Ca')],
#   'Ti': [('Ti', 'Ti'), ('B', 'P')],
#   'e':  [('H', 'F'), ('O', 'Mg'), ('N', 'Al')]}

# Then a "visual" analysis shows that the pair Rn-Ar stands out:
#    - Both atoms always occur together in a target molecule
#    - They only occur one time in those target molecules
#    - Y only appears in Rn-Ar-molecules of length 6
#    - If Y isn't in a Rn-Ar molecule, then the Rn-Ar-molecule has length 4
# And: Every other replacment molecule has length 2

RnAr_mapping = {}
for a, ms in mapping.items():
    for m in ms:
        if "Rn" in m or "Ar" in m:
            RnAr_mapping.setdefault(a, set()).add(m)

RnAr_values = set().union(*RnAr_mapping.values())
assert all(
    ("Rn" in m and "Ar" in m)  # Always: together
        and (sum(a == "Rn" or a == "Ar" for a in m) == 2)  # Always: only once
    for m in RnAr_values
)
assert all(
    len(m) == 6  # Always: Rn-Y-Ar molecules have atom count 6
    for ms in mapping.values()
    for m in ms
    if "Y" in m
)
assert all(  # Always: Rn-Ar-molecules have atom count 4
    len(m) == 4
    for m in RnAr_values
    if "Y" not in m
)
assert all(  # All non-Rn-Ar molecules have atom count 2
    len(m) == 2
    for ms in mapping.values()
    for m in ms
    if "Ar" not in m
)

#  => Under the assumption that the medicine molecule is actually producable
#  (which seems a nesecarry puzzle condition), it is obvious that every
#    - Rn-Y-Ar replacement increases the atom count by 5
#    - Rn-Ar replacement increases the atom count by 3
#    - other replacement increases the atom count by 1


def part_2(medicine):
    RnYArs = medicine.count("Y")
    RnArs = medicine.count("Rn") - RnYArs
    singletons = len(medicine) - RnYArs * 5 - RnArs * 3
    
    return RnYArs + RnArs + singletons - 1


solution = part_2(medicine)
assert solution == 207
print(solution)
