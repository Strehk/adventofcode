from collections import Counter
from typing import Set
from load_data import load_puzzle_input
import pandas as pd
import numpy as np
import re

lines = load_puzzle_input("4", sample=False)

df = pd.DataFrame([list(x) for x in lines])


# Task 1
def search_for_matches(string):
    matches = 0
    for i in range(len(string)):
        matches += 1 if re.match(r"XMAS|SAMX", string[i:]) else 0
    return matches


def search_for_horizontal_matches(df):
    matches = 0
    for i, row in df.iterrows():
        matches += search_for_matches("".join(row))
    return matches


def search_for_vertical_matches(df):
    matches = 0
    for i, row in df.items():
        matches += search_for_matches("".join(row))
    return matches


def search_for_diagonal_matches(df):
    matches = 0
    np_array = df.to_numpy()
    np_array_flipped = np.flip(np_array, 0)
    for i in range(len(np_array)):
        variant_1 = "".join(np_array.diagonal(i))
        variant_2 = "".join(np_array_flipped.diagonal(i))
        matches += search_for_matches(variant_1)
        matches += search_for_matches(variant_2)
        if i == 0:
            continue
        variant_3 = "".join(np_array.diagonal(-i))
        variant_4 = "".join(np_array_flipped.diagonal(-i))
        matches += search_for_matches(variant_3)
        matches += search_for_matches(variant_4)

    return matches


hor = search_for_horizontal_matches(df)
ver = search_for_vertical_matches(df)
dia = search_for_diagonal_matches(df)

print(hor)
print(ver)
print(dia)
print(hor + ver + dia)


# Task 2
def find_xmas_cross(df):
    total = 0
    np_array = df.to_numpy()
    height, width = np_array.shape

    for row in range(1, height - 1):
        for col in range(1, width - 1):
            diagonal1 = [
                np_array[row - 1][col - 1],
                np_array[row][col],
                np_array[row + 1][col + 1],
            ]
            diagonal2 = [
                np_array[row - 1][col + 1],
                np_array[row][col],
                np_array[row + 1][col - 1],
            ]

            d1 = "".join(diagonal1)
            d2 = "".join(diagonal2)
            
            valid_patterns = ["MAS", "SAM"]
            if (d1 in valid_patterns or d1[::-1] in valid_patterns) and (
                d2 in valid_patterns or d2[::-1] in valid_patterns
            ):
                total += 1

    return total

print()
print(find_xmas_cross(df))
