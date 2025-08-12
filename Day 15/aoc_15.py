from dataclasses import dataclass
from enum import Enum

@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x + other.x, self.y + other.y)
    def __mul__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x * other.x, self.y * other.y)

class Direction(Enum):
    LEFT = "<"
    RIGHT = ">"
    UP = "^"
    DOWN = "v"

    def get_direction_vector(self):
        match self:
            case Direction.LEFT: return Coordinate(-1, 0)
            case Direction.RIGHT: return Coordinate(1, 0)
            case Direction.UP: return Coordinate(0, -1)
            case Direction.DOWN: return Coordinate(0, 1)


class Entity_Type(Enum):
    ROBOT = 0
    BOX = 1
    WIDE_BOX = 2
    WALL = 3
    FLOOR = 4

    def __str__(self):
        return self.name.capitalize()


@dataclass
class Move:
    direction: Direction

@dataclass
class Moves:
    moves: list[Move]


@dataclass
class Entity:
    id: int
    entity_type: Entity_Type
    coordinates: list[Coordinate]
    gps_coordinates: list[int]

    def get_object_symbol(self):
        match self.entity_type:
            case Entity_Type.ROBOT: return "@"
            case Entity_Type.BOX: return "O"
            case Entity_Type.WIDE_BOX: return "[]"
            case Entity_Type.WALL: return "#"
            case Entity_Type.FLOOR: return "."
            case _: return "."

@dataclass
class Warehouse:
    width: int
    height: int
    entities: list[Entity]

    def __str__(self):
        rows = [["0"] * self.width for _ in range(self.height)]
        for y, row in enumerate(rows):
            x = 0
            while x < len(row):
                entity = self.find_entity_by_position(Coordinate(x, y))
                if entity is None:
                    x += 1
                    continue
                symbol = entity.get_object_symbol()
                if symbol == "[]":
                    rows[y][x] = symbol[0]
                    rows[y][x+1] = symbol[1]
                    x+=2
                    continue
                rows[y][x] = symbol
                x += 1
        lines = []
        for row in rows:
            line = "".join(row)
            lines.append(line)
        return "\n".join(lines)

    def get_robot(self):
        for entity in self.entities:
            if entity.entity_type == Entity_Type.ROBOT:
                return entity
        return None

    def find_entity_by_position(self, position: Coordinate):
        for entity in self.entities:
            for coordinate in entity.coordinates:
                if coordinate == position:
                    return entity
        return None

    def can_move(self, entity: Entity, dir_vector: Coordinate):
        entity_position = entity.coordinates[0]
        next_entity = self.find_entity_by_position(entity_position+dir_vector)
        if next_entity.entity_type == Entity_Type.BOX:
            return self.can_move(next_entity, dir_vector)
        if next_entity.entity_type == Entity_Type.WALL:
            return False
        if next_entity.entity_type == Entity_Type.FLOOR:
            return True
        return False

    def make_move(self, move: Move):
        print(move.direction, end=", ")
        robot = self.get_robot()
        dir_vector = move.direction.get_direction_vector()
        if self.can_move(robot, dir_vector):
            print("Robot can move!")
        else:
            print("Robot can't move!")





def main():
    warehouse_data = load_file("small_warehouse_example.txt")
    warehouse = create_warehouse(warehouse_data)
    print(warehouse)
    moves_data = load_file("small_robot_moves_example.txt")
    moves = create_moves(moves_data)
    warehouse.make_move(moves.moves[0])
    warehouse.make_move(moves.moves[3])
    warehouse.make_move(moves.moves[1])
    warehouse.make_move(moves.moves[6])
    for entity in warehouse.entities:
        print(entity)

def create_moves(moves_data:list[list[str]]):
    moves = []
    for row in moves_data:
        for move_str in row:
            direction = Direction(move_str)
            move = Move(direction)
            moves.append(move)
    return Moves(moves)


def create_warehouse(warehouse_data: list[list[str]]):
    width, height = len(warehouse_data[0]), len(warehouse_data)
    entities = []
    entity_id = 0
    for y, row in enumerate(warehouse_data):
        x = 0
        while x < len(row):
            gps_coordinates = [y * 100 + x]
            coordinates = [Coordinate(x, y)]
            if row[x] == "@":
                e = Entity(entity_id, Entity_Type.ROBOT, coordinates, gps_coordinates)
                entities.append(e)
                robot = e
            if row[x] == "[":
                x += 1
                coordinates.append(Coordinate(x, y))
                gps_coordinates.append(y * 100 + x)
                e = Entity(entity_id, Entity_Type.WIDE_BOX, coordinates, gps_coordinates)
                entities.append(e)
            if row[x] == "O":
                e = Entity(entity_id, Entity_Type.BOX, coordinates, gps_coordinates)
                entities.append(e)
            if row[x] == "#":
                e = Entity(entity_id, Entity_Type.WALL, coordinates, gps_coordinates)
                entities.append(e)
            if row[x] == ".":
                e = Entity(entity_id, Entity_Type.FLOOR, coordinates, gps_coordinates)
                entities.append(e)
            x += 1
            entity_id += 1
    warehouse = Warehouse(width, height, entities)
    return warehouse

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
    return data

if __name__ == "__main__":
    main()