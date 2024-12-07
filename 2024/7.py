from typing import List
from load_data import load_puzzle_input
from tqdm import tqdm

lines = load_puzzle_input("7", sample=False)


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def connect(a, b):
    return int(str(a) + str(b))


def try_combination(numbers: List[int], operators: List[str]) -> int:
    result = numbers[0]
    for i, operator in enumerate(operators):
        if operator == "+":
            result = add(result, numbers[i + 1])
        elif operator == "*":
            result = multiply(result, numbers[i + 1])
        elif operator == "||":
            result = connect(result, numbers[i + 1])
    return result


def try_all_combinations_task_1(numbers: List[int], target: int) -> bool:
    for i in range(2 ** (len(numbers) - 1)):
        operators = []
        for j in range(len(numbers) - 1):
            if i & (1 << j):
                operators.append("+")
            else:
                operators.append("*")
        if try_combination(numbers, operators) == target:
            return True
    return False


def try_all_combinations_task_2(numbers: List[int], target: int) -> bool:
    for i in range(3 ** (len(numbers) - 1)):
        operators = []
        for j in range(len(numbers) - 1):
            if i % 3 == 0:
                operators.append("+")
            elif i % 3 == 1:
                operators.append("*")
            else:
                operators.append("||")
            i = i // 3
        if try_combination(numbers, operators) == target:
            return True
    return False


# Task 1

sum = 0

for line in tqdm(lines):
    target_raw, numbers_raw = line.split(": ")
    numbers = [int(x) for x in numbers_raw.split(" ")]
    target = int(target_raw.strip().replace(":", ""))
    if try_all_combinations_task_1(numbers, target):
        sum += target

print(sum)

# Task 2

sum = 0

for line in tqdm(lines):
    target_raw, numbers_raw = line.split(": ")
    numbers = [int(x) for x in numbers_raw.split(" ")]
    target = int(target_raw.strip().replace(":", ""))
    if try_all_combinations_task_2(numbers, target):
        sum += target

print(sum)
