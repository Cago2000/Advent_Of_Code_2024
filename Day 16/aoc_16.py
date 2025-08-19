from enum import Enum
import numpy as np
from dataclasses import dataclass
import heapq
from itertools import count

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
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


    def get_direction_vector(self):
        match self:
            case Direction.NORTH: return Coordinate(0, -1)
            case Direction.EAST: return Coordinate(1, 0)
            case Direction.SOUTH: return Coordinate(0, 1)
            case Direction.WEST: return Coordinate(-1, 0)



@dataclass
class Reindeer:
    position: Coordinate
    direction: Direction = Direction.EAST
    score: int = 0

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


    def move_reindeer(self, commit: bool = True):
        new_position = self.reindeer.position + self.reindeer.direction.get_direction_vector()
        if self.layout[new_position.y, new_position.x].walkable:
            self.reindeer.position = new_position
            if commit:
                self.reindeer.score += 1

    def rotate_reindeer_clockwise(self, commit: bool = True):
        self.reindeer.direction = Direction((self.reindeer.direction.value + 1) % len(Direction))
        if commit:
            self.reindeer.score += 1000

    def rotate_reindeer_counterclockwise(self, commit: bool = True):
        self.reindeer.direction = Direction((self.reindeer.direction.value - 1) % len(Direction))
        if commit:
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


def dijkstra_best_path(maze: Maze):
    start = maze.reindeer.position
    start_dir = maze.reindeer.direction

    heap = []
    counter = count()
    heapq.heappush(heap, (0, next(counter), start, start_dir))

    visited = dict()
    prev_states = dict()
    end_pos = None
    best_score = None

    while heap:
        score, _, pos, direction = heapq.heappop(heap)

        cell = maze.layout[pos.y, pos.x]
        if isinstance(cell, End):
            end_pos = pos
            best_score = score
            break

        state_key = (pos.x, pos.y, direction.value)
        if state_key in visited and visited[state_key] <= score:
            continue
        visited[state_key] = score

        new_pos = pos + direction.get_direction_vector()
        if maze.layout[new_pos.y, new_pos.x].walkable:
            key = (new_pos.x, new_pos.y, direction.value, score + 1)
            prev_states.setdefault(key, []).append((pos.x, pos.y, direction.value, score))
            heapq.heappush(heap, (score + 1, next(counter), new_pos, direction))

        new_dir = Direction((direction.value + 1) % len(Direction))
        key = (pos.x, pos.y, new_dir.value, score + 1000)
        prev_states.setdefault(key, []).append((pos.x, pos.y, direction.value, score))
        heapq.heappush(heap, (score + 1000, next(counter), pos, new_dir))

        new_dir = Direction((direction.value - 1) % len(Direction))
        key = (pos.x, pos.y, new_dir.value, score + 1000)
        prev_states.setdefault(key, []).append((pos.x, pos.y, direction.value, score))
        heapq.heappush(heap, (score + 1000, next(counter), pos, new_dir))

    tiles_in_best_paths = set()
    stack = [(end_pos.x, end_pos.y, start_dir.value, best_score)]
    while stack:
        x, y, dir_val, score = stack.pop()
        tiles_in_best_paths.add((x, y))

        for prev in prev_states.get((x, y, dir_val, score), []):
            prev_x, prev_y, prev_dir_val, prev_score = prev
            if prev_score + (1 if (prev_x, prev_y) != (x, y) else 1000) == score:
                stack.append(prev)

    return tiles_in_best_paths, best_score


def main():
    maze_data = load_file("maze.txt")
    maze = create_maze(maze_data)

    tiles, best_score = dijkstra_best_path(maze)
    print(f"Minimum Score: {best_score}")
    print(f"Tiles in any best path: {len(tiles)}")



if __name__ == "__main__":
    main()