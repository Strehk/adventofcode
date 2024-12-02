from typing import Tuple, List, Literal
from misc import start_program
import sys
from tqdm import tqdm
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

sys.setrecursionlimit(100000)


class Pipe:
    def __init__(self, type: str, position: Tuple[str, str]) -> None:
        self.type = type
        self.position: Tuple[str, str] = position

        self.up: bool = type == "|" or type == "J" or type == "L" or type == "S"
        self.down: bool = type == "|" or type == "F" or type == "7" or type == "S"
        self.right: bool = type == "-" or type == "L" or type == "F" or type == "S"
        self.left: bool = type == "-" or type == "J" or type == "7" or type == "S"

        self.start: bool = type == "S"
        self.empty: bool = type == "."
        self.enclosed: bool = False
        self.open: bool = False

        self.connected_pipes: List[Pipe] = []

    @property
    def number_of_connections(self) -> int:
        return len(self.connected_pipes)

    def add_connected_pipe(self, pipe) -> None:
        if pipe not in self.connected_pipes:
            self.connected_pipes.append(pipe)

    def __str__(self) -> str:
        return f"Pipe of type {self.type} at position {self.position} with {len(self.connected_pipes)} connections"


def find_pipe(pipes: List[Pipe], position: Tuple[str, str]) -> Pipe:
    try:
        pipe = next(pipe for pipe in pipes if pipe.position == position)
    except StopIteration:
        return None
    return pipe


def check_pipe_connection(
    origin_pipe: Pipe,
    pipe_to_check: Pipe,
    pipe_to_check_dir: Literal["u", "d", "l", "r"],
) -> bool:
    if origin_pipe.up and pipe_to_check.down and pipe_to_check_dir == "u":
        return True
    elif origin_pipe.down and pipe_to_check.up and pipe_to_check_dir == "d":
        return True
    elif origin_pipe.right and pipe_to_check.left and pipe_to_check_dir == "r":
        return True
    elif origin_pipe.left and pipe_to_check.right and pipe_to_check_dir == "l":
        return True
    return False


def check_surroundings(all_pipes: List[Pipe], pipe: Pipe) -> bool:
    x, y = pipe.position
    up = find_pipe(all_pipes, (x, y + 1))
    down = find_pipe(all_pipes, (x, y - 1))
    right = find_pipe(all_pipes, (x + 1, y))
    left = find_pipe(all_pipes, (x - 1, y))

    if up and check_pipe_connection(pipe, up, "u"):
        pipe.add_connected_pipe(up)
    if down and check_pipe_connection(pipe, down, "d"):
        pipe.add_connected_pipe(down)
    if right and check_pipe_connection(pipe, right, "r"):
        pipe.add_connected_pipe(right)
    if left and check_pipe_connection(pipe, left, "l"):
        pipe.add_connected_pipe(left)


def walk_pipes(
    all_pipes: List[Pipe],
    init_pipe: Pipe or List[Pipe],
    steps: int = 0,
    visited_pipes: List[Pipe] = None,
) -> bool:
    if not isinstance(init_pipe, Pipe):
        if any(pipe.start for pipe in init_pipe) and steps > 2:
            return steps
        init_pipe = next(pipe for pipe in init_pipe if pipe not in visited_pipes)

    print(f"Now walking {init_pipe}")
    if visited_pipes == None:
        visited_pipes = []
    visited_pipes.append(init_pipe)

    steps = walk_pipes(all_pipes, init_pipe.connected_pipes, steps + 1, visited_pipes)

    return steps


def is_enclosed(all_pipes: List[Pipe], max_x: int, max_y: int, coordinate: Tuple[int, int]) -> bool:
    matrix = [[0 for _ in range(max_x)] for _ in range(max_y)]  # Correct dimensions: max_x columns, max_y rows

    for pipe in all_pipes:
        x, y = pipe.position
        matrix[y][x] = 0 if pipe.empty else 1

    grid = Grid(matrix=matrix)
    start_x, start_y = coordinate
    if not (0 <= start_x < max_x and 0 <= start_y < max_y):
        return False  # Coordinate is outside the grid

    start = grid.node(start_x, start_y)

    # Check path to edges
    for x in range(max_x):  # Checking for top and bottom edges
        for y in [0, max_y - 1]:
            if matrix[y][x] == 0:  # Check [row][column] with correct indices
                end = grid.node(x, y)
                finder = AStarFinder()
                path, _ = finder.find_path(start, end, grid)
                if path:
                    return False

    for y in range(max_y):  # Checking for left and right edges
        for x in [0, max_x - 1]:
            if matrix[y][x] == 0:  # Check [row][column] with correct indices
                end = grid.node(x, y)
                finder = AStarFinder()
                path, _ = finder.find_path(start, end, grid)
                if path:
                    return False

    return True


def area_count(all_pipes: List[Pipe], max_x: int, max_y: int) -> int:
    count = 0

    for pipe in tqdm(all_pipes):
        if pipe.empty:
            enclosed = is_enclosed(all_pipes, max_x, max_y, pipe.position)
            if enclosed:
                count += 1
                pipe.enclosed = True
            else:
                pipe.open = True

    return count


def main_1(data):
    pipes: List[Pipe] = []

    for y, line in enumerate(data[::-1]):
        for x, char in enumerate(line):
            if char != " " and char != ".":
                pipes.append(Pipe(char, (x, y)))

    start = next(pipe for pipe in pipes if pipe.start)

    print("Checking surroundings")
    for pipe in tqdm(pipes):
        check_surroundings(pipes, pipe)

    print("\nWalking Pipes")
    print(walk_pipes(pipes, start) / 2)


def main_2(data):
    #TODO Unfinished
    print("Warning: This method is unfinished and will not work correctly\n\n")
    pipes: List[Pipe] = []

    for y, line in enumerate(data[::-1]):
        for x, char in enumerate(line):
            if char != " ":
                pipes.append(Pipe(char, (x, y)))

    print("\nChecking surroundings")
    for pipe in tqdm(pipes):
        check_surroundings(pipes, pipe)

    print("\nCounting areas")
    print(area_count(pipes, len(data[0]), len(data)))
    
    for y in range(len(data))[::-1]:
        for x in range(len(data[0])):
            pipe = find_pipe(pipes, (x, y))
            if pipe:
                if pipe.enclosed:
                    print("I", end="")
                elif pipe.open:
                    print(".", end="")
                elif pipe.start:
                    print("░", end="")
                else:
                    print("█", end="")
        print()


if __name__ == "__main__":
    start_program([main_1, main_2])
