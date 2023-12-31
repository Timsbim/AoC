# Day 3
from pprint import pprint
from collections import Counter


# Reading input
with open("2021/day_03_input.csv", "r") as file:
    numbers = [line.rstrip() for line in file]
"""
numbers = [
    "00100", "11110", "10110", "10111",  "10101", "01111", "00111", "11100",
    "10000", "11001", "00010", "01010"
]
"""


# Part 1
print("Part 1:")

bins = "0b" + "".join(
    str(int(column.count("1") >= len(numbers) / 2)) for column in zip(*numbers)
)
gamma = int(bins, 2)
epsilon = (2 ** (len(bins) - 2) - 1) ^ gamma
print(f"(1) {gamma = },\n(2) {epsilon = },\n(3) {gamma * epsilon = }")


# Part 2
print("Part 2:")

for diagnostic in ("generator", "scrubber"):
    remaining_numbers = numbers[:]
    for i in range(len(numbers[0])):
        count = Counter(number[i] for number in remaining_numbers)
        if diagnostic == "generator":
            bit = "1" if count["0"] <= count["1"] else "0"
        else:
            bit = "0" if count["0"] <= count["1"] else "1"
        remaining_numbers = [
            number for number in remaining_numbers if number[i] == bit
        ]
        if len(remaining_numbers) == 1:
            break
    if diagnostic == "generator":
        generator = int(remaining_numbers[0], 2)
    else:
        scrubber = int(remaining_numbers[0], 2)

print(
    f"(1) {generator = },\n(2) {scrubber = },\n(3) {generator * scrubber = }"
)