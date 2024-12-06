input_map = open('map.txt', 'r')
map_list = []
directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
current_index = 0


def get_next_dir():
    global current_index
    current_index += 1
    current_index %= 4
    return list(directions)[current_index]


def get_key_by_value(searched_value):
    for key, value in directions.items():
        if searched_value == value:
            return key


def walk():
    i, j = get_current_position()
    a, b = get_current_direction()
    if i+a >= len(map_list) or i+a < 0 or j+b >= len(map_list[i]) or j+b < 0:
        return True
    if map_list[i+a][j+b] == '#':
        dir = get_next_dir()
        map_list[i][j] = dir
        return False
    map_list[i+a][j+b] = map_list[i][j]
    map_list[i][j] = 'X'
    return False


def walk_to_end():
    done = False
    while not done:
        done = walk()
    print("End reached!")
    count = 0
    for line in map_list:
        count += line.count('X')
        print(line)
    count += 1 #Last position
    print(count)





def get_current_position():
    for i, line_list in enumerate(map_list):
        for j, char in enumerate(line_list):
            if char != '.' and char != '#' and char != 'X':
                return i, j


def get_current_direction():
    i, j = get_current_position()
    return directions[map_list[i][j]]


def main():
    for line in input_map:
        line_list = []
        for char in line.strip():
            line_list.append(char)
        map_list.append(line_list)
    walk_to_end()


if __name__ == "__main__":
    main()