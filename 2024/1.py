from collections import Counter
from load_data import load_puzzle_input

lines = load_puzzle_input("1")

left_list = [int(x.split("   ")[0].strip()) for x in lines]
right_list = [int(x.split("   ")[1].strip()) for x in lines]

# Task 1

distances = []

left_list_copy = left_list.copy()
right_list_copy = right_list.copy()

while len(left_list_copy) > 0:
    left_min = min(left_list_copy)
    right_min = min(right_list_copy)
    
    left_index = left_list_copy.index(left_min)
    right_index = right_list_copy.index(right_min)
    
    distances.append(abs(left_min - right_min))
    
    left_list_copy.pop(left_index)
    right_list_copy.pop(right_index)

print(sum(distances))

# Task 2

similarity_score = 0

for num in left_list:
    counter = Counter(right_list)
    similarity_score += num * counter[num]
    
print(similarity_score)