from load_data import load_puzzle_input
from functools import reduce

from operator import mul
import re


def multiply_list(input):
    filtered = list(filter(lambda x: "mul" in x, re.findall(r"mul\(\d+\,\d+\)", input)))
    
    extracted = [
        x.replace("mul", "").replace("(", "").replace(")", "").split(",") for x in filtered
    ]

    converted = [[int(x) for x in y] for y in extracted]

    return [reduce(mul, x) for x in converted]


lines = load_puzzle_input("3", sample=False)
input = "".join(lines)

# Task 1
print(sum(multiply_list(input)))

# Task 2

dos = re.finditer(r"do\(\)", input)
donts = re.finditer(r"don't\(\)", input)

dos = [x.start() for x in dos]
donts = [x.start() for x in donts]

result = []
safe = True
last = 0
for i in range(len(input)):
    if safe:
        if i in donts:
            safe = False
            result.append(sum(multiply_list(input[last:i])))
    else:
        if i in dos:
            safe = True
            last = i

print(sum(result))