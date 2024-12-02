from collections import Counter
from load_data import load_puzzle_input

lines = load_puzzle_input("1")

left_list = [int(x.split("   ")[0].strip()) for x in lines]
right_list = [int(x.split("   ")[1].strip()) for x in lines]

# Task 1
distances = [abs(x - y) for x, y in zip(sorted(left_list), sorted(right_list))]
print(sum(distances))

# Task 2
similarity_score = sum(num * right_list.count(num) for num in left_list)
print(similarity_score)
