# Day 6
from pprint import pprint


# Reading input
with open("2021/input/day_06.csv", "r") as file:
    timers_input = [int(n) for n in file.read().strip().split(",")]
#timers_input = [3, 4, 3, 1, 2]


# Part 1
print("Part 1:")

timers = {t: timers_input.count(t) for t in range(9)}
for d in range(1, 81):
    spawners = timers[0]
    for t in timers:
        if t < 8:
            timers[t] = timers[t + 1]
    timers[6] += spawners
    timers[8] = spawners
num_of_fish = sum(timers.values())
print(f"Number of fish after 80 days: {num_of_fish}")


#Part 2
print("Part 2:")

timers = {t: timers_input.count(t) for t in range(9)}
for d in range(1, 257):
    spawners = timers[0]
    for t in timers:
        if t < 8:
            timers[t] = timers[t + 1]
    timers[6] += spawners
    timers[8] = spawners
num_of_fish = sum(timers.values())
print(f"Number of fish after 256 days: {num_of_fish}")
