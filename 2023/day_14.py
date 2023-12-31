# --------------------------------------------------------------------------- #
#    Day 14                                                                   #
# --------------------------------------------------------------------------- #

DAY = 14
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2023/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    mountain = file.read()
if EXAMPLE:
    print(mountain)

# --------------------------------------------------------------------------- #
#    Helper                                                                   #
# --------------------------------------------------------------------------- #

def rows_to_string(rows):
    return "\n".join(map("".join, rows))


def tilt_north(rows):
    height, width = len(rows), len(rows[0])
    for c in range(width):
        for r0 in range(1, height):
            if rows[r0][c] != "O":
                continue
            for r in range(r0 - 1, -2, -1):
                if rows[r][c] != ".":
                    break
            if (r1 := r + 1) != r0:
                rows[r1][c], rows[r0][c] = "O", "." 
    return rows


def full_cycle_tilt(rows):
    height, width = len(rows), len(rows[0])
    
    for c in range(width):  # North
        for r0 in range(1, height):
            if rows[r0][c] != "O":
                continue
            for r in range(r0 - 1, -2, -1):
                if r == -1 or rows[r][c] != ".":
                    break
            if (r1 := r + 1) != r0:
                rows[r1][c], rows[r0][c] = "O", "." 

    for row in rows:  # West
        for c0, char in enumerate(row):
            if c0 == 0 or char != "O":
                continue
            for c in range(c0 - 1, -2, -1):
                if c == -1 or row[c] != ".":
                    break
            if (c1 := c + 1) != c0:
                row[c1], row[c0] = "O", "." 
    
    for c in range(width):  # South
        for r0 in range(height - 2, -1, -1):
            if rows[r0][c] != "O":
                continue
            for r in range(r0 + 1, height + 1):
                if r == height or rows[r][c] != ".":
                    break
            if (r1 := r - 1) != r0:
                rows[r1][c], rows[r0][c] = "O", "." 

    for row in rows:  # East
        for c0 in range(width - 1, -1, -1):
            if row[c0] != "O":
                continue
            for c in range(c0 + 1, width + 1):
                if c == width or row[c] != ".":
                    break
            if (c1 := c - 1) != c0:
                row[c1], row[c0] = "O", "." 

    return rows


def weight(rows):
    height, width = len(rows), len(rows[0])
    weight = 0
    for r in range(height):
        weight += sum(1 for c in range(width) if rows[r][c] == "O") * height
        height -= 1
    return weight

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(mountain):
    rows = [*map(list, mountain.splitlines())]
    return weight(tilt_north(rows))


solution = part_1(mountain)
assert solution == (136 if EXAMPLE else 108614)
print(solution)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(mountain):
    rows = [*map(list, mountain.splitlines())]
    n, strings, hashs = 0, [], {}
    while True:
        rows = full_cycle_tilt(rows)
        string = rows_to_string(rows)
        hashed = hash(string)
        if start := hashs.get(hashed, False):
            break
        strings.append(string)
        hashs[hashed] = n
        n += 1
    
    offset = (1_000_000_000 - start - 1) % (n - start)
    return weight(strings[start + offset].splitlines())


solution = part_2(mountain)
assert solution == (64 if EXAMPLE else 96447)
print(solution)
