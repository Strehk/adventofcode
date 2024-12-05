from load_data import load_puzzle_input
from functools import cmp_to_key

lines = load_puzzle_input("5", sample=False)


# Task 1
def read_lines():
    instructions_finished = False
    instructions = []
    ordering = []

    for line in lines:
        if line == "":
            instructions_finished = True
            continue

        if instructions_finished:
            ordering.append([int(x) for x in line.split(",")])
        else:
            before_page, after_page = line.split("|")
            instructions.append((int(before_page.strip()), int(after_page.strip())))

    return instructions, ordering


def check_order(instructions, order):
    for i, num in enumerate(order):
        count = 0
        for before_page, after_page in instructions:
            if after_page == num and before_page in order[:i]:
                count += 1
        if count != i:
            return False
    return True


instructions, ordering = read_lines()

score = 0
for order in ordering:
    if check_order(instructions, order):
        middle = order[len(order) // 2]
        score += middle

print(score)


# Task 2


def custom_compare(a, b):
    for before_page, after_page in instructions:
        if a == after_page and b == before_page:
            return 1
        if a == before_page and b == after_page:
            return -1
    return 0


def reorder(order):
    sort = sorted(order, key=cmp_to_key(custom_compare))
    print(order, sort)
    return sort


score = 0
for order in ordering:
    new_order = reorder(order)
    if not order == new_order:
        middle = new_order[len(new_order) // 2]
        score += middle

print(score)
