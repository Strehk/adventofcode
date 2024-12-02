from load_data import load_puzzle_input

lines = load_puzzle_input("2", sample=False)


def analizer(nums):
    prev = None
    decr = None
    for i, num in enumerate(nums):
        if i == 0:
            prev = num
            continue
        if abs(num - prev) > 3 or num == prev:
            break

        if i == 1:
            decr = num - prev < 0
        else:
            if decr and num - prev > 0:
                break
            if not decr and num - prev < 0:
                break

        prev = num
    else:
        return True
    return False


def damper(nums):
    if analizer(nums):
        return True  # Return Safe Reports if the list is already safe

    for i, num in enumerate(nums):
        copy = nums.copy()
        copy.pop(i)
        if analizer(copy):
            return True
    return False


# Task 1

safe_reports = 0
for line in lines:
    nums = [int(x) for x in line.split(" ")]
    if analizer(nums):
        safe_reports += 1

print(safe_reports)


# Task 2

safe_reports = 0
for line in lines:
    nums = [int(x) for x in line.split(" ")]
    if damper(nums):
        safe_reports += 1

print(safe_reports)
