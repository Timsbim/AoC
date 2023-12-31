# Day 1


# Reading input
with open("2021/day_01_input.csv", "r") as file:
    depths = [int(line) for line in file]


# Part 1
print(
    sum(
        n2 > n1 for n1, n2 in zip(depths[:-1], depths[1:])
    )
)


# Part 2
print(
    sum(
        sum(depths[i:i + 3]) > sum(depths[j:j + 3])
        for i, j in zip(range(1, len(depths) - 2), range(len(depths) - 3))
    )
)
depths_sums = [sum(depths[i:i + 3]) for i in range(len(depths) - 2)]
print(len(depths), len(depths_sums))
print(
    sum(
        n2 > n1 for n1, n2 in zip(depths_sums[:-1], depths_sums[1:])
    )
)
