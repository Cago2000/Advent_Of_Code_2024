import copy
from collections import OrderedDict

directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
dir_index = 0
loop_counter = 0


def get_next_dir_key():
    global dir_index
    dir_index += 1
    dir_index %= 4
    return list(directions)[dir_index]


def get_next_dir_value():
    global dir_index
    dir_index += 1
    dir_index %= 4
    return directions[list(directions)[dir_index]]


def get_key_by_value(searched_value):
    for key, value in directions.items():
        if searched_value == value:
            return key


def get_current_position(map_list):
    for i, line_list in enumerate(map_list):
        for j, char in enumerate(line_list):
            if char != '.' and char != '#' and char != 'X':
                return i, j


def get_current_direction(map_list):
    i, j = get_current_position(map_list)
    return directions[map_list[i][j]]


def walk(map_list):
    global loop_counter
    i, j = get_current_position(map_list)
    a, b = get_current_direction(map_list)
    if i+a >= len(map_list) or i+a < 0 or j+b >= len(map_list[i]) or j+b < 0:
        map_list[i][j] = 'X'
        return True
    if map_list[i+a][j+b] == '#':
        next_dir = get_next_dir_key()
        map_list[i][j] = next_dir
        return False
    map_list[i+a][j+b] = map_list[i][j]
    map_list[i][j] = 'X'
    return False


def walk_to_end(map_list, i, j):
    global dir_index
    states = []
    done = False
    while not done:
        done= walk(map_list)
    map_list[i][j] = 'X'
    dir_index = 0
    count = 0
    for line in map_list:
        count += line.count('X')
    return count


def check_loop(map_list, states, i, j, a, b):
    global loop_counter
    if i+a >= len(map_list) or i+a < 0 or j+b >= len(map_list[i]) or j+b < 0:
        return True, states, i, j, a, b
    if map_list[i+a][j+b] == '#':
        (a, b) = get_next_dir_value()
    else:
        i = i+a
        j = j+b
    if ((i, j), (a, b)) in states:
        loop_counter += 1
        return True, states, i, j, a, b
    else:
        states.add(((i, j), (a, b)))
    return False, states, i, j, a, b


def check_loop_to_end(map_list, i, j):
    states = set()
    a, b = -1, 0
    states.add(((i, j), (-1, 0)))
    done = False
    while not done:
        done, states, i, j, a, b = check_loop(map_list, states, i, j, a, b)


def main():
    path = 'map.txt'
    input_map = open(path, 'r')
    map_list = []
    for line in input_map:
        line_list = []
        for char in line.strip():
            line_list.append(char)
        map_list.append(line_list)
    x, y = get_current_position(map_list)
    counter = walk_to_end(map_list, x, y)
    print(f'Part One: Counter: {counter}')
    map_list_copy = copy.deepcopy(map_list)
    global dir_index
    iter_counter = 0
    for i, line_list in enumerate(map_list_copy):
        for j, char in enumerate(line_list):
            if char == 'X':
                print(iter_counter)
                iter_counter += 1
                map_list_copy[i][j] = '#'
                check_loop_to_end(map_list_copy, x, y)
                map_list_copy[i][j] = 'X'
                dir_index = 0
    print(f'Part Two: Loop Counter: {loop_counter}')


if __name__ == "__main__":
    main()
