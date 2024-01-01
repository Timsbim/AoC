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

RnAr_mapping = {
    a: [m for m in ms if ("Rn" in m) or ("Ar" in m)]  # Rn OR Ar in molecule
    for a, ms in mapping.items()
}
RnAr_values = set().union(*RnAr_mapping.values())
assert all(
    ("Rn" in m and "Ar" in m)  # Always: together
        and (sum(a == "Rn" or a == "Ar" for a in m) == 2)  # Always: only once
        and (m[1] == "Rn" and m[-1] == "Ar")  # Always: Rn second & Ar last
    for m in RnAr_values
)
assert all(
    m[1:] == ("Rn", "F", "Y", "F", "Ar")  # Always: Y in (*, Rn, F, Y, F, Ar)
    for ms in mapping.values()
    for m in ms
    if "Y" in m
)
assert all(  # Always: if Y not in Rn-Ar-molecule then F between Rn and Ar
    m[1:] in (("Rn", "F", "Ar"), ("Rn", "Mg", "Ar"))
    for m in RnAr_values
    if "Y" not in m
)

#  Rn-Ar mapping part of the graph:
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

rev_RnAr_mapping = {}
for a, ms in RnAr_mapping.items():
    for m in ms:
        key = (m[0], "Y") if "Y" in m else (m[0], m[2])
        #rev_RnAr_mapping.setdefault(key, set()).add(a)
        rev_RnAr_mapping[key] = a
#pprint(rev_RnAr_mapping)

non_RnAr_mapping = {
    a: [m for m in ms if "Rn" not in m]
    for a, ms in mapping.items()
    if any("Rn" not in m for m in ms)
}

# Non-Rn-Ar-mapping part of the graph:
#
#  {'Al': [('Th', 'F')],
#   'B':  [('Ti', 'B'), ('B', 'Ca')],
#   'Ca': [('P', 'B'), ('Si', 'Th'), ('Ca', 'Ca')],
#   'F':  [('Ca', 'F'), ('Si', 'Al'), ('P', 'Mg')],
#   'H':  [('H', 'Ca'), ('O', 'B'), ('N', 'Th')],
#   'Mg': [('Ti', 'Mg'), ('B', 'F')],
#   'N':  [('H', 'Si')],
#   'O':  [('O', 'Ti'), ('H', 'P')],
#   'P':  [('Ca', 'P'), ('P', 'Ti')],
#   'Si': [('Ca', 'Si')],
#   'Th': [('Th', 'Ca')],
#   'Ti': [('Ti', 'Ti'), ('B', 'P')],
#   'e':  [('N', 'Al'), ('H', 'F'), ('O', 'Mg')]}

non_RnAr_starts = {m[0] for ms in RnAr_mapping.values() for m in ms}

#  Left-of-Rn starting atoms: N, O, Ti, Si, Th, P

def find_left_rims():
    left_rims = {}
    for a in non_RnAr_starts:
        visited, paths = {a}, [a]
        while paths:
            next_paths = []
            for a0 in paths:
                for m in non_RnAr_mapping[a]:
                    a1 = m[-1]
                    if a1 not in visited:
                        next_paths.append(a1)
                        visited.add(a1)
            paths = next_paths
        left_rims[a] = visited

    return left_rims


left_rim_mapping = find_left_rims()

#  Left-Rn-rim possibilities based on starting rim:
#
#  {'N':  {'Si', 'N'},
#   'O':  {'Ti', 'P', 'O'},
#   'P':  {'Ti', 'P'},
#   'Si': {'Si'},
#   'Th': {'Ca', 'Th'},
#   'Ti': {'Ti', 'P'}}

left_rims = set().union(*left_rim_mapping.values())

#  Possible left-Rn-rims: Ca, N, O, 'P, Si, Th, Ti

left_rim_origins = {}
for a0, ats in left_rim_mapping.items():
    for a1 in ats:
        left_rim_origins.setdefault(a1, set()).add(a0)

#  Mapping of left-Rn-rim to possible origins:
#
#  {'Ca':  {'Th'},
#    'N':  {'N'},
#    'O':  {'O'},
#    'P':  {'Ti', 'P', 'O'},
#    'Si': {'N', 'Si'},
#    'Th': {'Th'},
#    'Ti': {'Ti', 'P', 'O'}}

F_Mg_left_ends = {}
for a0 in "F", "Mg":
    visited, paths = {a0}, [a0]
    while paths:
        a1 = paths.pop()
        for m in mapping[a1]:
            a2 = m[0]
            if a2 not in visited:
                visited.add(a2)
                paths.append(a2)
    F_Mg_left_ends[a0] = visited

#  {'F':  {'P', 'Si', 'F', 'Ca'},
#   'Mg': {'B', 'Mg', 'Ti'}}


rimRnAr_origins = {}
for a0, ats in left_rim_origins.items():
    for a1 in ats:
        for switch in "F", "Mg", "Y":
            if (value := rev_RnAr_mapping.get((a1, switch))) is not None:
                rimRnAr_origins.setdefault((a0, switch), set()).add(value)
#pprint(rimRnAr_origins)


def first_RnAr_group(molecule):
    level, path = 0, []
    for i, atom in enumerate(molecule):
        if atom == "Rn":
            if level == 0:
                i0 = i
            level += 1
        elif atom == "Ar":
            level -= 1
            if level == 0:
                return i0, i


@cache
def min_non_RnAr(atom, molecule):
    target_len = len(molecule)
    minimum = float("inf")
    paths = [(0, (atom,))]
    while paths:
        steps, m = paths.pop()
        for i, a in enumerate(m):
            left, right = m[:i], m[i+1:]
            for repl_as in non_Rn_Ar_mapping[a]:
                next_m = left + repl_as + right
                if next_m == molecule:
                    minimum = min(minimum, steps + 1)
                elif len(next_m) < target_len:
                    paths.append((steps + 1, next_m))

    return minimum


@cache
def minimize(molecule):
    if "Rn" not in molecule:
        return min_non_RnAr("e", molecule)
    i0, i1 = first_RnAr_group(molecule)
    rim, inner = molecule[i0-1], molecule[i0+1:i1]
    left, right = molecule[:i0-1], molecule[i1+1:]
    if "Rn" not in inner:
        if "Y" in inner:
            iY = inner.index("Y")
            steps = min_non_RnAr("F", inner[:iY])
            steps += min_non_RnAr("F", inner[iY+1:])
            repls = rimRnAr_origins.get((rim, "Y"), set())
            reductions = (left + repl + right for repl in repls)
            return steps + 1 + min(map(minimize, reductions))
        else:
            minimum = float("inf")
            for switch in "F", "Mg":
                steps = min_non_RnAr(switch, inner)
                repls = rimRnAr_origins.get((rim, switch), [])
                reductions = (left + repl + right for repl in repls)
                steps += 1 + min(map(minimize, reductions))
                minimum = min(minimum, steps)
            return minimum
    


def part_2():
    pass


#solution = part_2()
#assert solution == (3 if not EXAMPLE else )
#print(solution)


def first_RnAr_groups(molecule):
    groups = []
    level, path = 0, []
    for i, atom in enumerate(molecule):
        if atom == "Rn":
            if level == 0:
                i0 = i
            level += 1
        elif atom == "Ar":
            level -= 1
            if level == 0:
                groups.append((i0, i))

    return tuple(groups)


for i0, i1 in first_RnAr_groups(medicine):
    print(medicine[i0-1:i1+1])
