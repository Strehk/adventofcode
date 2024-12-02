import os


def load_puzzle_input(task: str, sample: bool = False):
    file_name = "sample.txt" if sample else "input.txt"
    with open(f"{os.path.dirname(__file__)}/data/{task}/{file_name}") as file:
        return file.read().splitlines()
