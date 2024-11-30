# --------------------------------------------------------------------------- #
#    Day 7                                                                    #
# --------------------------------------------------------------------------- #

import re

DAY = 7
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2022/input/day_{DAY:0>2}"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    lines = file.read().splitlines()

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

re_console = re.compile(
    r"^(?:(?P<cd>\$ cd (?P<todir>.*))|(?P<file>(?P<size>\d+)(?:.*)))$"
)

dirs = {".": {"size": 0}}
stack = [dirs["."]]
dir = stack[-1]
for line in lines:
    match = re_console.match(line)
    if not match:
        continue
    match = re_console.match(line).groupdict()
    if match["cd"]:
        todir = match["todir"]
        if todir == "/":
            stack = [dirs["."]]
        elif todir == "..":
            stack.pop()
        else:
            dir[todir] = {"size": 0}
            stack.append(dir[todir])
        dir = stack[-1]
    elif match["file"]:
        dir["size"] += int(match["size"])
        

def sizes(dirs):
    size = dirs.get("size", 0)
    result = []
    for name, subdir in dirs.items():
        if name == "size":
            continue
        subsizes = sizes(subdir)
        size += subsizes[0]
        result.extend(subsizes)
    return [size] + result

sizes = sizes(dirs)
print(sum(size for size in sizes if size < 100_000))  # 1513699

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

hurdle = max(sizes[0] - 40_000_000, 0)
print(min(size for size in sizes if size >= hurdle))  # 7991939
