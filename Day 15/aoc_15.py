from dataclasses import dataclass
from enum import Enum
from stack import Stack

@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x + other.x, self.y + other.y)

@dataclass
class Action:
    coordinates: tuple[Coordinate, Coordinate]

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
class Entity:
    entity_type: Entity_Type
    coordinates: list[Coordinate]

    def get_symbol(self):
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
                entity = self.get_entity_by_position(Coordinate(x, y))
                if entity is None:
                    x += 1
                    continue
                symbol = entity.get_symbol()
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
        lines.append("")
        return "\n".join(lines)

    def get_robot(self):
        for entity in self.entities:
            if entity.entity_type == Entity_Type.ROBOT:
                return entity
        return None

    def get_action_stack(self, entity: Entity, dir_vector: Coordinate, actions: Stack):
        entity_position = entity.coordinates[0]
        next_entity = self.get_entity_by_position(entity_position + dir_vector)
        print(next_entity)
        if next_entity.entity_type == Entity_Type.WALL:
            return Stack()
        if next_entity.entity_type == Entity_Type.BOX:
            action = Action((entity.coordinates[0], next_entity.coordinates[0]))
            actions.push(action)
            return self.get_action_stack(next_entity, dir_vector, actions)
        if next_entity.entity_type == Entity_Type.WIDE_BOX:
            action = Action((entity.coordinates[0], next_entity.coordinates[0]))
            actions.push(action)
            return self.get_action_stack(next_entity, dir_vector, actions)
        if next_entity.entity_type == Entity_Type.FLOOR:
            action = Action((entity.coordinates[0], next_entity.coordinates[0]))
            actions.push(action)
            return actions
        return actions

    def perform_action(self, action: Action):
        print(action)
        first, second = action.coordinates
        self.swap_by_position(first, second)

    def swap_by_position(self, pos1: Coordinate, pos2: Coordinate):
        index1, index2 = self.get_index_of_entity_by_position(pos1), self.get_index_of_entity_by_position(pos2)
        self.entities[index2].coordinates, self.entities[index1].coordinates = self.entities[index1].coordinates, self.entities[index2].coordinates

    def get_entity_by_position(self, position: Coordinate):
        for entity in self.entities:
            if position in entity.coordinates:
                return entity
        return None

    def get_index_of_entity_by_position(self, pos: Coordinate):
        for i, entity in enumerate(self.entities):
            if entity.coordinates[0] == pos:
                return i
        return None

    def calculate_gps_coordinate_sum(self):
        gps_coordinate_sum = 0
        for entity in self.entities:
            if entity.entity_type == Entity_Type.BOX:
                x, y = entity.coordinates[0].x, entity.coordinates[0].y
                gps_coordinate_sum += y*100+x
        return gps_coordinate_sum

def main():
    warehouse_data = load_file("warehouse_example.txt")
    warehouse = create_warehouse(warehouse_data)
    moves_data = load_file("robot_moves_example.txt")
    moves = create_moves(moves_data)
    print(warehouse)
    for move in moves:
        print(move)
        actions = warehouse.get_action_stack(warehouse.get_robot(), move.get_direction_vector(), Stack())
        for i in range(len(actions.stack)):
            warehouse.perform_action(actions.pop())
        print(warehouse)
    gps_coordinate_sum = warehouse.calculate_gps_coordinate_sum()
    print(gps_coordinate_sum)


def create_moves(moves_data:list[list[str]]):
    moves = []
    for row in moves_data:
        for move_str in row:
            direction = Direction(move_str)
            moves.append(direction)
    return moves


def create_warehouse(warehouse_data: list[list[str]]):
    width, height = len(warehouse_data[0]), len(warehouse_data)
    entities = []
    entity_id = 0
    for y, row in enumerate(warehouse_data):
        x = 0
        while x < len(row):
            coordinates = [Coordinate(x, y)]
            if row[x] == "@":
                e = Entity(Entity_Type.ROBOT, coordinates)
                entities.append(e)
            if row[x] == "[":
                x += 1
                coordinates.append(Coordinate(x, y))
                e = Entity(Entity_Type.WIDE_BOX, coordinates)
                entities.append(e)
            if row[x] == "O":
                e = Entity(Entity_Type.BOX, coordinates)
                entities.append(e)
            if row[x] == "#":
                e = Entity(Entity_Type.WALL, coordinates)
                entities.append(e)
            if row[x] == ".":
                e = Entity(Entity_Type.FLOOR, coordinates)
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