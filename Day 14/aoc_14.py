import re
from dataclasses import dataclass


@dataclass
class Robot:
    id: int
    position: tuple[int, int]
    velocity: tuple[int, int]

def main():
    robots_data = load_file("robots_example.txt")
    robots = get_robot_data(robots_data)
    width, height = 11, 7
    draw_tiles(robots, width, height)
    seconds = 100
    tiles = []
    for _ in range(seconds):
        robots = move_robots(robots, width, height)
        tiles =draw_tiles(robots, width, height)
    calculate_safety_score(tiles)

def calculate_safety_score(tiles):
    width, height = len(tiles[0]), len(tiles)
    print(width, height)
    left_width, right_width = (0, width//2-1), (width//2+1, width-1)
    upper_height, lower_height = (0, height//2-1), (height//2+1, height-1)
    print(left_width, right_width)
    print(upper_height, lower_height)


def draw_tiles(robots: dict[int, Robot], width: int, height: int):
    tiles = []
    for j in range(height):
        row = []
        for i in range(width):
            number_of_robots = 0
            for _, robot in robots.items():
                if robot.position == (i, j):
                    number_of_robots += 1
            row.append(number_of_robots)
        tiles.append(row)

    return tiles


def move_robots(robots: dict[int, Robot], width: int, height: int):
    for _, robot in robots.items():
        move_robot(robot, width, height)
    return robots

def move_robot(robot: Robot, width: int, height: int):
    robot_x, robot_y = robot.position
    robot_x_velocity, robot_y_velocity = robot.velocity
    if robot_x < 0 or robot_x >= width: robot_x %= width
    if robot_y < 0 or robot_y >= height: robot_y %= height
    if robot_x_velocity < 0 or robot_x_velocity >= width: robot_x_velocity %= width
    if robot_y_velocity < 0 or robot_x_velocity >= height: robot_y_velocity %= height
    new_robot_x, new_robot_y = (robot_x+robot_x_velocity)%width, (robot_y+robot_y_velocity)%height
    robot.position = new_robot_x, new_robot_y
    print(robot_x, robot_y, robot_x_velocity, robot_y_velocity, new_robot_x, new_robot_y)


def get_robot_data(robots_data):
    robots = {}
    for i, line in enumerate(robots_data):
        line = line.removesuffix("\n")
        d = re.findall(r'-?\d+', line)
        d = [int(x) for x in d]
        robot_position = (d[0], d[1])
        robot_velocity = (d[2], d[3])
        robot_id = i
        robot = Robot(robot_id, robot_position, robot_velocity)
        robots[i] = robot

    return robots
def load_file(path: str):
    file = open(path, 'r')
    data = []
    for line in file:
        if line == "\n":
            continue
        data.append(line)
    return data
if __name__ == "__main__":
    main()