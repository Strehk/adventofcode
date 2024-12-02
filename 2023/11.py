from misc import start_program
from typing import List
from collections import deque
from tqdm import tqdm


class Universe:
    def __init__(self, raw_data: List[str]) -> None:
        self.universe_map: [[Galaxy or str]] = []
        self.galaxies: [Galaxy] = []
        self.parse_raw_data(raw_data)

    def parse_raw_data(self, raw_data: List[str]):
        id_count = 1
        for line_index, line in enumerate(raw_data):
            self.universe_map.append([])
            for column_index, column in enumerate(line):
                if column == "#":
                    galaxy = Galaxy(id_count, (line_index, column_index))
                    self.galaxies.append(galaxy)
                    self.universe_map[line_index].append(galaxy)
                    id_count += 1
                else:
                    self.universe_map[line_index].append(None)
                    
    def update_all_galaxy_coordinates(self):
        print("\nUpdating all galaxy coordinates")
        for line_index, line in tqdm(enumerate(self.universe_map)):
            for column_index, column in tqdm(enumerate(line), leave=False):
                if column != None:
                    column.update_coordinates((line_index, column_index))
                    
                    
    def calculate_total_distances(self) -> int:
        print("\nCalculating total distances")
        distances = []
        for galaxy in tqdm(self.galaxies):
            for other_galaxy in tqdm(self.galaxies, leave=False):
                if galaxy != other_galaxy:
                    distances.append(galaxy.calculate_distance(other_galaxy))
        return sum(distances)

    def expand(self, factor: int):
        print("\nExpanding universe")
        for _ in range(2):
            inserts = []
            for index, line in enumerate(self.universe_map):
                if all([coordinate == None for coordinate in line]):
                    inserts.append(index)

            insert_count = 0
            for index in tqdm(inserts):
                for _ in tqdm(range(factor - 1), leave=False):
                    self.universe_map.insert(index + insert_count, ([None for _ in line]))
                    insert_count += 1
                
            self.invert_map()
        
        self.update_all_galaxy_coordinates()

    def invert_map(self):
        self.universe_map = [list(row) for row in tqdm(zip(*self.universe_map), desc="Inverting map")]

    def __str__(self) -> str:
        string = ""
        for line in self.universe_map:
            for coordinate in line:
                if coordinate == None:
                    string += "."
                else:
                    string += str(coordinate)
            string += "\n"
        return string



class Galaxy:
    def __init__(self, id, coordinates: (int, int)) -> None:
        self.id: int = id
        self.coordinates: (int, int) = coordinates
        self.distances: {Galaxy: int} = {}

    def __str__(self) -> str:
        return str(self.id)
    
    def calculate_distance(self, galaxy: object) -> int:
        if galaxy.id not in self.distances.keys():
            distance = manhattan_distance(self.coordinates, galaxy.coordinates)
            self.add_distance(galaxy, distance)
            galaxy.add_distance(self, distance)
            return distance
        else:
            return 0
        
    def update_coordinates(self, coordinates: (int, int)):
        self.coordinates = coordinates
    
    def add_distance(self, galaxy: object, distance: int):
        self.distances[galaxy.id] = distance
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Galaxy):
            return False
        return self.id == o.id
    

def manhattan_distance(start: (int, int), end: (int, int)) -> int:
    return  abs(start[0] - end[0]) + abs(start[1] - end[1])

def bfs(universe: Universe, galaxy_pair: (Galaxy, Galaxy)):
    start, end = galaxy_pair
    rows, cols = len(universe.universe_map), len(universe.universe_map[0])
    visited = set()
    queue = deque([(start.coordinates, 0)])

    while tqdm(queue, leave=False):
        (x, y), distance = queue.popleft()

        if (x, y) == end.coordinates:
            return distance + 1

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), distance + 1))

def main_1(data):
    universe = Universe(data)
    universe.expand(2)
    print("\nTotal distances:")
    print(universe.calculate_total_distances())


def main_2(data):
    universe = Universe(data)
    universe.expand(10000)
    print("\nTotal distances:")
    print(universe.calculate_total_distances())


if __name__ == "__main__":
    start_program([main_1, main_2])
