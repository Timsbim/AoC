# Day 18
from pprint import pprint
from io import StringIO
import re
from itertools import product

DAY = 18
EXAMPLE = False


# Preparation
file_name = f"2021/day_{DAY:0>2}_input"
if EXAMPLE:
    file_name += "_example"
file_name += ".csv"


# Reading input
with open(file_name, "r") as file:
    numbers = [line.rstrip() for line in file]
# pprint(numbers)


# Helper functions

class Number:
    _re_pair = re.compile(r"\[(\d+),(\d+)\]")
    _re_num_left = re.compile(r"(\d+)\D*$")
    _re_num_right = re.compile(r"(\d+)")
    _re_ge10 = re.compile(r"(\d\d+)")

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.number)})"

    def __init__(self, number):
        self.number = number

    def explode(self):
        for match in self._re_pair.finditer(self.number):
            level = Number.level(self.number[:match.start()])
            if level >= 4:
                left, right = (int(number) for number in match.groups())
                num_left = self.number[:match.start()]
                num_right = self.number[match.end():]
                match = self._re_num_left.search(num_left)
                if match:
                    incr = len(match[1]) 
                    num_left = (
                        num_left[:match.start()]
                        + str(int(match[1]) + left)
                        + num_left[match.start() + incr:]
                    )
                match = self._re_num_right.search(num_right)
                if match:
                    num_right = (
                        num_right[:match.start()]
                        + str(right + int(match[1]))
                        + num_right[match.end():]
                    )
                self.number = num_left + "0" + num_right
                return True
        return False

    def needs_explosion(self):
        for match in self._re_pair.finditer(self.number):
            if Number.level(self.number[:match.start()]) >= 4:
                return True
        return False

    def split(self):
        match = self._re_ge10.search(self.number)
        if match:
            half, remainder = divmod(int(match[1]), 2)
            self.number = (
                self.number[:match.start()]
                + f"[{half},{half + remainder}]"
                + self.number[match.end():]
            )

    def needs_splitting(self):
        return self._re_ge10.search(self.number) is not None
    
    def reduce(self):
        while True:
            if not any(
                [self.needs_explosion(), self.needs_splitting()]
            ):
                break
            if self.needs_explosion():
                self.explode()
                continue
            if self.needs_splitting():
                self.split()

    def __add__(self, other):
        if not isinstance(other, Number):
            return NotImplemented
        new_number = Number(f"[{self.number},{other.number}]")
        new_number.reduce()
        return new_number

    def magnitude(self):
        return Number._magnitude(eval(self.number))
    
    @staticmethod
    def level(string):
        return string.count("[") - string.count("]")

    @staticmethod
    def _magnitude(number):
        left, right = number
        left = left if isinstance(left, int) else Number._magnitude(left)
        right = right if isinstance(right, int) else Number._magnitude(right)
        return 3 * left + 2 * right


# Part 1
print("\nPart 1:")

numbers = [Number(number) for number in numbers]
result, *numbers = numbers
for number in numbers:
    result = result + number
print(result.number)
print(result.magnitude())
# 4207


# Part 2
print("\nPart 2:")

sums = [
    numbers[i] + numbers[j]
    for i, j in product(range(len(numbers)), repeat=2)
    if i != j
]
max_mag = max(number.magnitude() for number in sums)
print(max_mag)
# 4635
