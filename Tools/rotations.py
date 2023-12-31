from itertools import combinations, permutations
from pprint import pprint


def transpose(matrix):
    return tuple(zip(*matrix))


def mat_mul(matrix_1, matrix_2):
    result = []
    for row in matrix_1:
        new_row = []
        for col in zip(*matrix_2):
            new_row.append(sum(a * b for a, b in zip(row, col)))
        result.append(tuple(new_row))
    return tuple(result)


def get_3dim_cube_rotations():
    """ Builds all 3d cube rotation matrices"""
    # 1. Reflections sorted by determinant (+/-1)
    reflections = {-1: [], 1: [(1, 1, 1)]}
    for n in 1, 2, 3:  # Number of -1s in the diagonal
        reflections[(-1) ** n].extend(  # Determinant is -1^number of -1s
            tuple(-1 if i in minus else 1 for i in (0, 1, 2))
            for minus in combinations((0, 1, 2), n)
        )
    # 2. Take the permutaitions, get their determinant (-1^number of swaps)
    # and multiplicate them with the corresponding reflections
    rotations = []
    for p in permutations((0, 1, 2)):
        swaps = (i == p[j] and p[i] == j for i, j in ((0, 1), (0, 2), (1, 2)))
        for reflection in reflections[(-1) ** sum(swaps)]:
            rotation = tuple(
                tuple(r if j == i else 0 for j, r in enumerate(reflection))
                for i in p
            )
            rotations.append(rotation)
    return rotations


def get_ndim_cube_rotations(dim):
    # 1. Reflections sorted by determinant (+/-1)
    reflections = {-1: [], 1: [tuple(1 for _ in range(dim))]}
    for n in range(1, dim + 1):
        reflections[(-1) ** n].extend(
            tuple(-1 if i in minus else 1 for i in range(dim))
            for minus in combinations(range(dim), n)
        )
    # 2. Take the permutaitions, get their determinant (-1 ** number of swaps)
    # and multiplicate them with the corresponding reflections
    rotations = []
    for p in permutations(range(dim)):
        swaps = (
            i == p[j] and p[i] == j
            for i, j in combinations(range(dim), 2)
        )
        for reflection in reflections[(-1) ** sum(swaps)]:
            rotation = tuple(
                tuple(r if j == i else 0 for j, r in enumerate(reflection))
                for i in p
            )
            rotations.append(rotation)
    return rotations


def print_rotation(rotation):
    for row in rotation:
        print(" ".join(f"{n:2> }" for n in row))


pprint(get_3dim_cube_rotations())
