def diagonals(matrix):
    rows, cols = len(matrix), len(matrix[0])
    
    # Below main diagonal (inclusive)
    diags_below = tuple(
        tuple(matrix[d+c][c] for c in range(min(rows - d, cols)))
        for d in range(rows)
    )

    # Above main diagonal
    diags_above = tuple(
        tuple(matrix[r][r+d] for r in range(min(cols - d, rows)))
        for d in range(1, cols)
    )

    return diags_below, diags_above


def antidiagonals(matrix):
    rows, cols = len(matrix), len(matrix[0])

    # Above main anti-diagonal (inclusive)    
    diags_above = tuple(
        tuple(matrix[d-c][c] for c in range(min(d + 1, cols)))
        for d in range(rows - 1, -1, -1)
    )
    
    # Below main anti-diagonal
    diags_below = tuple(
        tuple(matrix[r][d-r] for r in range(rows - 1, max(-1, d - cols), -1))
        for d in range(rows, rows + cols - 1)
    )

    return diags_below, diags_above


def example(rows, cols):

    def print_row(row):
        return " ".join(f"{n},{m}" for n, m in row)
    
    matrix = tuple(
        tuple((row, col) for col in range(cols))
        for row in range(rows)
    )
    print(f"\n{rows}x{cols}-Matrix:", end="\n\n")
    for r in range(rows):
        print("  ", print_row(matrix[r]))
    
    print("\n Diagonals:", end="\n\n")
    below, above = diagonals(matrix)
    for n, diag in zip(range(cols-1, 0, -1), reversed(above)):
        print(f"   {n}:", print_row(diag))
    for n, diag in enumerate(below):
        print(f"   {n}:", print_row(diag))

    print("\n Anti-diagonals:", end="\n\n")
    below, above = antidiagonals(matrix)
    for n, diag in zip(range(rows-1, -1, -1), reversed(above)):
        print(f"   {n}:", print_row(diag))
    for n, diag in enumerate(below, start=1):
        print(f"   {n}:", print_row(diag))


if __name__ == "__main__":

    example(5, 3)
    #example(3, 5)
