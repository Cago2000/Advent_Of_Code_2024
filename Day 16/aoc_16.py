from enum import Enum
import numpy as np
from dataclasses import dataclass

@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x + other.x, self.y + other.y)


@dataclass
class Wall:
    coordinate: Coordinate
    symbol: str = "#"
    walkable: bool = False


@dataclass
class Tile:
    coordinate: Coordinate
    symbol: str = "."
    walkable: bool = True


@dataclass
class Start:
    coordinate: Coordinate
    symbol: str = "S"
    walkable: bool = True


@dataclass
class End:
    coordinate: Coordinate
    symbol: str = "E"
    walkable: bool = True


class Direction(Enum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3

    def get_direction_vector(self):
        match self:
            case Direction.EAST: return Coordinate(1, 0)
            case Direction.NORTH: return Coordinate(0, -1)
            case Direction.WEST: return Coordinate(-1, 0)
            case Direction.SOUTH: return Coordinate(0, 1)


@dataclass
class Reindeer:
    position: Coordinate
    score: int = 0
    direction: Direction = Direction.EAST


@dataclass
class Maze:
    layout: np.ndarray[object]
    reindeer: Reindeer

    def __str__(self) -> str:
        rows = []
        for y in range(self.layout.shape[0]):
            row_chars = []
            for x in range(self.layout.shape[1]):
                cell = self.layout[y, x]
                if cell is None:
                    row_chars.append(" ")
                    continue
                if self.reindeer.position == Coordinate(x, y):
                    row_chars.append("R")
                    continue
                row_chars.append(cell.symbol)
            rows.append("".join(row_chars))
        return "\n".join(rows)

    def move(self):
        new_position = self.reindeer.position + self.reindeer.direction.get_direction_vector()
        if self.layout[new_position.y, new_position.x].walkable:
            self.reindeer.position = new_position
            self.reindeer.score += 1

    def rotate(self):
        self.reindeer.direction = Direction((self.reindeer.direction.value+1) % len(Direction))
        self.reindeer.score += 1000


def load_file(path: str):
    file = open(path, 'r')
    data = []
    for line in file:
        if line == "\n":
            continue
        line = line.removesuffix("\n")
        row = []
        for c in line:
            row.append(c)
        data.append(row)
    return np.array(data)


def return_maze_object(character: str, coordinate: Coordinate):
    match character:
        case "#":
            return Wall(coordinate)
        case ".":
            return Tile(coordinate)
        case "E":
            return End(coordinate)
        case "S":
            return Start(coordinate)
        case _:
            return None


def create_maze(maze_data: np.ndarray):
    maze = np.empty_like(maze_data, dtype=object)
    reindeer_position = Coordinate(-1, -1)
    for y, row in enumerate(maze_data):
        for x, character in enumerate(row):
            maze_object = return_maze_object(character, Coordinate(x, y))
            if maze_object is None:
                continue
            if isinstance(maze_object, Start):
                reindeer_position = Coordinate(x, y)
            maze[y, x] = maze_object
    return Maze(maze, Reindeer(reindeer_position))


def main():
    maze_data = load_file("maze_example.txt")
    maze = create_maze(maze_data)
    print(maze)
    print(maze.reindeer)
    maze.rotate()
    maze.move()
    maze.move()
    maze.move()
    maze.move()
    print(maze)
    print(maze.reindeer)


if __name__ == "__main__":
    main()