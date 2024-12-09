# --------------------------------------------------------------------------- #
#    Day 9                                                                    #
# --------------------------------------------------------------------------- #

DAY = 9
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day", DAY)

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

if EXAMPLE:
    disk_map = "2333133121414131402"
else:
    with open("2024/input/day_09.txt", "r") as file:
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
        files[i], files[j] = files[j], "."
    return checksum(files)


print(solution := part_1(disk_map))
assert solution == (1928 if EXAMPLE else 6340197768906)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(disk_map):
    ID, files, occupied, free = -1, [], {}, {}
    for i, n in enumerate(disk_map):
        l, n, = len(files), int(n)
        container, key, item = (
            (free, l, ".") if i % 2 else (occupied, ID := ID + 1, ID)
        )
        container[key] = range(l, l + n)
        files.extend(item for _ in range(n))
    for ID, idxso in reversed(occupied.items()):
        i, l, found = idxso.start, len(idxso), False
        for j, idxsf in free.items():
            if i <= idxsf.start:
                break
            if l <= len(idxsf):
                found = True
                break
        if found:
            for k, l in zip(idxsf, idxso):
                files[k], files[l] = ID, "."
            if len(idxso) < len(idxsf):
                free[j] = range(idxsf.start + len(idxso), idxsf.stop)
            else:
                del free[j]
    return checksum(files)


print(solution := part_2(disk_map))
assert solution == (2858 if EXAMPLE else 6363913128533)
