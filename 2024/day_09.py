# --------------------------------------------------------------------------- #
#    Day 9                                                                    #
# --------------------------------------------------------------------------- #

DAY = 9
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

file_name = f"2024/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

if EXAMPLE:
    disk_map = "2333133121414131402"
else:
    with open(file_name, "r") as file:
        disk_map = file.read().rstrip()
    
# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #


def checksum(disk):
    s = 0
    for i, n in enumerate(disk):
        if n != ".":
            s += i * n
    return s


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1(disk_map):
    ID, files, occupied, free = -1, [], [], []
    for i, n in enumerate(disk_map):
        container, item = (free, ".") if i % 2 else (occupied, ID := ID + 1)
        l, n, = len(files), int(n)
        container.extend(range(l, l + n))
        files.extend(item for _ in range(n))
    for i, j in zip(free, reversed(occupied)):
        if j < i:
            break
        files[i] = files[j]
        files[j] = "."
    return checksum(files)


print(solution := part_1(disk_map))
assert solution == (1928 if EXAMPLE else 6340197768906)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(disk_map):
    ID, files, occupied, free = -1, [], [], {}
    for i, n in enumerate(disk_map):
        l, n, = len(files), int(n)
        idxs = range(l, l + n)
        if i % 2:
            item, free[l] = ".", idxs
        else:
            item = (ID := ID + 1)
            occupied.append((ID, idxs))
        files.extend(item for _ in range(n))
    while occupied:
        ID, idxs = occupied.pop()
        j, l, found = idxs.start, len(idxs), False
        for i, idxs1 in free.items():
            if j <= idxs1.start:
                break
            if l <= len(idxs1):
                found = True
                break
        if found:
            for k, l in zip(free[i], idxs):
                files[k], files[l] = ID, "."
            if len(idxs) < len(free[i]):
                free[i] = range(free[i].start + len(idxs), free[i].stop)
            else:
                del free[i]
    return checksum(files)


print(solution := part_2(disk_map))
assert solution == (2858 if EXAMPLE else 6363913128533)