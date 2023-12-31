# --------------------------------------------------------------------------- #
#    Day 19                                                                   #
# --------------------------------------------------------------------------- #
import re
import sys

from collections import Counter, deque
from functools import cache
from itertools import groupby
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
BASE = lines[-1]
MAPPING = {}
for line in lines[:-2]:
    left, right = line.split(" => ")
    MAPPING.setdefault(left, set()).add(right)

if EXAMPLE:
    print(BASE)
    pprint(MAPPING)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    return len({
        BASE[:m.start()] + ma + BASE[m.end():]
        for a, ms in MAPPING.items()
        for ma in ms
        for m in re.finditer(a if len(a) == 2 else f"{a}(?![a-z])", BASE)
    })


solution = part_1()
assert solution == (4 if EXAMPLE else 576)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="\n\n")

if EXAMPLE:
    print(3)  # Easy search through the graph
    sys.exit()

#pprint(MAPPING)

# Transform medicine and targets in MAPPING in tuple of atoms
re_atom = re.compile(r"[A-Z][a-z]|[A-Z]")
medicine = tuple(re_atom.findall(BASE))
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

# Then a "visual" analysis shows the that the pair Rn-Ar stands out:
#    - Both atoms always occur together in a target molecule
#    - They only occur one time in those target molecules
#    - Ar appears always somewhere after Rn
#    - Rn always at the 2. positon and Ar always at the end
#    - Y only appears in the following molecule Rn, F, Y, F, Ar
#    - If Y isn't in a Rn-Ar molecule, then the molecule has length 4 and the
#      atom between Rn and R is either F or Mg

Rn_Ar_mapping = {
    a: [m for m in ms if ("Rn" in m) or ("Ar" in m)]  # Rn OR Ar in molecule
    for a, ms in mapping.items()
}
Rn_Ar_values = set().union(*Rn_Ar_mapping.values())
assert all(
    ("Rn" in m and "Ar" in m)  # Always: together
        and (sum(a == "Rn" or a == "Ar" for a in m) == 2)  # Always: only once
        and (m[1] == "Rn" and m[-1] == "Ar")  # Always: Rn second & Ar last
    for m in Rn_Ar_values
)
assert all(
    m[1:] == ("Rn", "F", "Y", "F", "Ar")  # Always: Y in (*, Rn, F, Y, F, Ar)
    for ms in mapping.values()
    for m in ms
    if "Y" in m
)
assert all(  # Always: if Y not in Rn-Ar-molecule then F between Rn and Ar
    m[1:] in (("Rn", "F", "Ar"), ("Rn", "Mg", "Ar"))
    for m in Rn_Ar_values
    if "Y" not in m
)

#  The Rn-Ar mapping part of the graph:
#
#  {'Al': [('Th', 'Rn', 'F',  'Ar')],
#   'B':  [('Ti', 'Rn', 'F',  'Ar')],
#   'Ca': [('P',  'Rn', 'F',  'Ar'),
#          ('Si', 'Rn', 'Mg', 'Ar'),
#          ('Si', 'Rn', 'F',  'Y', 'F', 'Ar')],
#   'H':  [('O',  'Rn', 'F',  'Ar'),
#          ('N',  'Rn', 'Mg', 'Ar'),
#          ('N',  'Rn', 'F',  'Y', 'F', 'Ar')],
#   'O':  [('N',  'Rn', 'F',  'Ar')],
#   'P':  [('Si', 'Rn', 'F',  'Ar')]}


def find_matching_pairs(medicine):
    level, levels, path = 0, {}, []
    for i, atom in enumerate(medicine):
        if atom == "Rn":
            path.append(i)
            level += 1
        elif atom == "Ar":
            level -= 1
            levels.setdefault(level, []).append((path.pop(), i))

    return levels


#pprint(find_matching_pairs(medicine))


non_Rn_Ar_mapping = {
    a: [m for m in ms if "Rn" not in m]
    for a, ms in mapping.items()
    if any("Rn" not in m for m in ms)
}
#pprint(non_Rn_Ar_mapping)

non_Rn_Ar_starts = {m[0] for ms in Rn_Ar_mapping.values() for m in ms}
#pprint(non_Rn_Ar_starts)







"""
med_atom_count = len(medicine)
med_char_count = len(BASE)
med_unchange_counts = Counter(a for a in medicine if a in unchangeables)
#print(med_atom_count, med_char_count, med_unchange_counts)

def valid_molecule(molecule):
    if med_atom_count <= len(molecule):
        return False
    if med_char_count < sum(map(len, molecule)):
        return False
    return (
        Counter(a for a in molecule if a in unchangeables)
            <= med_unchange_counts
    )


minimum = float("inf")
paths = [(0, ("e",))]
while paths:
    steps, molecule = paths.pop()
    for i, atom in enumerate(molecule):
        if atom in unchangeables:
            continue
        left, right = molecule[:i], molecule[i+1:]
        for next_atoms in mapping[atom]:
            next_molecule = left + next_atoms + right
            if next_molecule == medicine:
                minimum = min(minimum, steps + 1)
                print(minimum)
            elif valid_molecule(next_molecule):
                paths.append((steps + 1, next_molecule))
print(minimum)
"""



def part_2():
    pass


solution = part_2()
#assert solution == (3 if not EXAMPLE else )
print(solution)
