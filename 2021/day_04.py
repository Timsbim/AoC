# Day 4
from pprint import pprint
from collections import defaultdict


# Reading input
with open("2021/day_04_input.csv", "r") as file:
    draw_numbers = list(
        reversed([int(n) for n in next(file).strip().split(",")])
    )
    rows = defaultdict(list)
    no = -1
    for line in file:
        line = line.strip()
        if not line:
            no += 1
            continue
        rows[no].append(list(map(int, line.split())))
# print(draw_numbers)
boards = dict.fromkeys(rows.keys())
for no, rows in rows.items():
    boards[no] = {"rows": rows, "columns": list(zip(*rows))}
# pprint(boards)


# Part 1
print("Part 1:")

draws = draw_numbers[:]
numbers = set()
score_board = {
    no: {"rows": [0] * 5, "columns": [0] * 5} for no in range(len(boards))
}
finished = False
while draws:
    draw = draws.pop()
    if draw not in numbers:
        numbers.add(draw)
        for no, board in boards.items():
            for dim in ("rows", "columns"):
                scores = score_board[no][dim]
                for arr in board[dim]:
                    matches = [i for i, n in enumerate(arr) if n == draw]
                    for i in matches:
                        scores[i] += 1
                    if not finished and any(s == 5 for s in scores):
                        finished = True
                        winning_board = no
                        final_number = draw
    if finished:
        break

score = sum(
    number
    for row in boards[winning_board]["rows"]
    for number in row
    if number not in numbers
)
final_score = final_number * score
# pprint(score_board)
print(
    f"(1) {winning_board = },\n(2) {final_number = },\n(3) {score = },\n"
    f"(4) {final_score = }"
)


# Part 2
print("Part 2:")

draws = draw_numbers[:]
numbers = set()
score_board = {
    no: {"rows": [0] * 5, "columns": [0] * 5, "finished": False}
    for no in range(len(boards))
}
finished = [False] * len(boards)
while draws:
    draw = draws.pop()
    if draw not in numbers:
        numbers.add(draw)
        for no, board in boards.items():
            if score_board[no]["finished"]:
                continue
            for dim in ("rows", "columns"):
                scores = score_board[no][dim]
                for arr in board[dim]:
                    matches = [i for i, n in enumerate(arr) if n == draw]
                    for i in matches:
                        scores[i] += 1
                    if any(s == 5 for s in scores):
                        score_board[no]["finished"] = True
                        finished[no] = True
                        final_board = no
    
    if all(finished):
        final_number = draw
        break

score = sum(
    number
    for row in boards[final_board]["rows"]
    for number in row
    if number not in numbers
)
final_score = final_number * score
# pprint(score_board)
print(
    f"(1) {final_board = },\n(2) {final_number = },\n(3) {score = },\n"
    f"(4) {final_score = }"
)
