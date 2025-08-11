from dataclasses import dataclass
from enum import Enum


@dataclass
class Box:
    id: int
    coordinate: tuple[int, int]
    gps_coordinate: int

@dataclass
class Robot:
    id: int
    coordinate: tuple[int, int]
    gps_coordinate: int

class Direction(Enum):
    LEFT = "<"
    RIGHT = ">"
    UP = "^"
    DOWN = "v"

def main():
    warehouse = load_file("warehouse.txt")
    print_warehouse(warehouse)
    boxes, robots = get_boxes_data(warehouse)

    for _, box in boxes.items():
        print(box)
    print()
    for _, robot in robots.items():
        print(robot)
    print()

    robot_moves = load_file("robot_moves.txt")
    for row in robot_moves:
        for move in row:
            warehouse = make_move(Direction(move), robots[0], warehouse)
    boxes, robots = get_boxes_data(warehouse)
    sum_of_gps_coordinates = calculate_sum_of_gps_coordinates(boxes)
    print(sum_of_gps_coordinates)

def calculate_sum_of_gps_coordinates(boxes: dict[int, Box]):
    sum_of_gps_coordinates = 0
    for _, box in boxes.items():
        sum_of_gps_coordinates += box.gps_coordinate
    return sum_of_gps_coordinates


def make_move(move: Direction, robot: Robot, warehouse: list[list[str]]):
    robot_x, robot_y = robot.coordinate
    shift = 1
    match move:
        case Direction.LEFT:
            while warehouse[robot_y][robot_x - shift] == "O":
                shift += 1
            if warehouse[robot_y][robot_x - shift] == "#":
                return warehouse
            if shift != 1:
                warehouse[robot_y][robot_x - shift], warehouse[robot_y][robot_x-1] = warehouse[robot_y][robot_x-1], warehouse[robot_y][robot_x - shift]
            warehouse[robot_y][robot_x], warehouse[robot_y][robot_x-1] = warehouse[robot_y][robot_x-1], warehouse[robot_y][robot_x]
            robot.coordinate = (robot_x-1, robot_y)
            return warehouse
        case Direction.RIGHT:
            while warehouse[robot_y][robot_x + shift] == "O":
                shift += 1
            if warehouse[robot_y][robot_x + shift] == "#":
                return warehouse
            if shift != 1:
                warehouse[robot_y][robot_x + shift], warehouse[robot_y][robot_x + 1] = warehouse[robot_y][robot_x + 1], warehouse[robot_y][robot_x + shift]
            warehouse[robot_y][robot_x], warehouse[robot_y][robot_x + 1] = warehouse[robot_y][robot_x + 1], warehouse[robot_y][robot_x]
            robot.coordinate = (robot_x+1, robot_y)
            return warehouse
        case Direction.UP:
            while warehouse[robot_y - shift][robot_x] == "O":
                shift += 1
            if warehouse[robot_y - shift][robot_x] == "#":
                return warehouse
            if shift != 1:
                warehouse[robot_y - shift][robot_x], warehouse[robot_y - 1][robot_x] = warehouse[robot_y - 1][robot_x], warehouse[robot_y - shift][robot_x]
            warehouse[robot_y][robot_x], warehouse[robot_y - 1][robot_x] = warehouse[robot_y - 1][robot_x], warehouse[robot_y][robot_x]
            robot.coordinate = (robot_x, robot_y-1)
            return warehouse
        case Direction.DOWN:
            while warehouse[robot_y + shift][robot_x] == "O":
                shift += 1
            if warehouse[robot_y + shift][robot_x] == "#":
                return warehouse
            if shift != 1:
                warehouse[robot_y + shift][robot_x], warehouse[robot_y + 1][robot_x] = warehouse[robot_y + 1][robot_x], warehouse[robot_y + shift][robot_x]
            warehouse[robot_y][robot_x], warehouse[robot_y + 1][robot_x] = warehouse[robot_y + 1][robot_x], warehouse[robot_y][robot_x]
            robot.coordinate = (robot_x, robot_y+1)
            return warehouse


def get_boxes_data(warehouse: list[list[str]]):
    box_id = 0
    boxes = {}
    robots = {}
    robot_id = 0
    for y, row in enumerate(warehouse):
        for x, c in enumerate(row):
            gps_coordinate = y * 100 + x
            coordinate = (x, y)
            if c == "O":
                box = Box(box_id, coordinate, gps_coordinate)
                boxes[box_id] = box
                box_id += 1
            if c == "@":
                robot = Robot(robot_id, coordinate, gps_coordinate)
                robots[robot_id] = robot
                robot_id += 1
    return boxes, robots

def print_warehouse(warehouse):
    for row in warehouse:
        print("".join(row))
    print()

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