import sys
from load_data import load_puzzle_input
import numpy as np
from enum import Enum
from tqdm import tqdm

lines = load_puzzle_input("6", sample=False)

map_matrix = np.array([np.array(list(line)) for line in lines])
width, height = map_matrix.shape

starting_position = (
    next(i for i, x in enumerate(map_matrix) if "^" in x),
    next(i for i, x in enumerate(map_matrix.T) if "^" in x),
)


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


# Part 1


def rotate_right(direction):
    return {
        Direction.UP: Direction.RIGHT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.UP,
    }[direction]


def move(position, direction):
    next_x, next_y = position[0] + direction.value[0], position[1] + direction.value[1]

    if map_matrix[next_x, next_y] == "#":
        return position, rotate_right(direction)
    elif map_matrix[next_x, next_y] in [".", "X", "^"]:
        return (next_x, next_y), direction
    else:
        print(f"Error, stepping on {map_matrix[next_x, next_y]} at {next_x, next_y}")
        raise ValueError("Invalid map")


current_position = starting_position
current_direction = Direction.UP
visit = set()

while True:
    # if the current position is out of bounds, we are done
    # visit.add((current_position))
    # map_matrix[current_position] = "X"

    try:
        current_position, current_direction = move(current_position, current_direction)
    except ValueError:
        break


print(len(visit))
with open("6.txt", "w") as f:
    f.write("\n".join("".join(row) for row in map_matrix))
