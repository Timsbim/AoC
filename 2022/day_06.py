# --------------------------------------------------------------------------- #
#    Day 6                                                                    #
# --------------------------------------------------------------------------- #

DAY = 6
EXAMPLE = False

# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #

file_name = f"2022/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

with open(file_name, "r") as file:
    buffer = file.read().strip()
#print()

# --------------------------------------------------------------------------- #
#    Helper functions                                                         #
# --------------------------------------------------------------------------- #

def start_position(buffer, buff_len=4):
    for i in range(len(buffer) - buff_len):
        if len(set(buffer[i:i + buff_len])) == buff_len:
            return i + buff_len

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 1:")

print(start_position(buffer))  # 1538
        
# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("\nPart 2:")

print(start_position(buffer, 14))  # 2315