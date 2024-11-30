# Day 8
from pprint import pprint
from collections import defaultdict


# Reading input
with open("2021/input/day_08.csv", "r") as file:
    signals = []
    for line in file:
        parts = line.split("|")
        signals.append([part.split() for part in parts])

# pprint(inp)
# pprint(out)

encoding = {
    0: "abcefg", 1: "cf", 2: "acdeg", 3: "acdfg", 4: "bcdf",
    5: "abdfg", 6: "abdefg", 7: "acf", 8: "abcdefg", 9: "abcdfg"
}
decoding = defaultdict(list)
for signal in encoding.values():
    decoding[len(signal)].append(signal)
pprint(decoding)


# Part 1
print("Part 1:")

lengths = {len(encoding[n]): encoding[n] for n in {1, 4, 7, 8}}
print(lengths)
num_easy = sum(len(seq) in lengths for _, row in signals for seq in row)
print(f"Number of digits 1, 4, 7, or 8: {num_easy}")


# Part 2
print("Part 2:")

lengths = defaultdict(list)
output_values = 0
for inp, out in signals:
    mapping = dict.fromkeys(range(10))
    for signal in inp:
        length, s = len(signal), set(signal)
        if length == 2:
            mapping[1] = s
        elif length == 3:
            mapping[7] = s
        elif length == 4:
            mapping[4] = s
        elif length == 7:
            mapping[8] = s
        else:
            lengths[len(signal)].append(signal)
    a = mapping[7] - mapping[1]
    abcdf = mapping[4] | mapping[7]
    abd = abcdf - mapping[1]
    bd = abd - a
    for i, signal in enumerate(lengths[6]):
        s = set(signal)
        if abcdf <= s:
            index = i
            mapping[9] = s
            g = s - abcdf
    lengths[6].pop(index)
    for signal in lengths[6]:
        s = set(signal)
        if abd <= s:
            mapping[6] = s
        else:
            mapping[0] = s
    del lengths[6]
    cfg = mapping[1] | g
    for signal in lengths[5]:
        s = set(signal)
        if abd <= s:
            mapping[5] = s
        elif cfg <= s:
            mapping[3] = s
        else:
            mapping[2] = s
    del lengths[5]
    number = ""
    for signal in out:
        s = set(signal)
        for key, value in mapping.items():
            if s == value:
                number += str(key)
                break
    output_values += int(number)

print(f"{output_values = }")