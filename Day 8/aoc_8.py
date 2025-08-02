def main():
    path = 'map.txt'
    input_map = open(path, 'r')
    map_list = []
    for line in input_map:
        map_list.append(list(char for char in line.strip()))

    antenna_pairs = {}
    antenna_id = 0
    for y1, line1 in enumerate(map_list):
        for x1, antenna1 in enumerate(line1):
            if antenna1 != "." and antenna1 != "#":
                for y2, line2 in enumerate(map_list):
                    for x2, antenna2 in enumerate(line2):
                        if y2 == y1 or x2 == x1: continue
                        if antenna2 == antenna1:
                            antenna_pair = {
                                "a1": (x1, y1),
                                "a2": (x2, y2),
                                "distance": (x2-x1, y2-y1),
                                "freq": antenna1
                            }
                            antenna_pairs[antenna_id] = antenna_pair
                            antenna_id += 1

    width, height = len(map_list[0]), len(map_list)
    antinode_map = [["." for _ in range(height)] for _ in range(width)]

    for antenna_id in antenna_pairs:
        antenna_pair = antenna_pairs[antenna_id]
        print(antenna_pair)
        ax1, ay1 = antenna_pair["a1"]
        dx, dy = antenna_pair["distance"]
        idx, idy = dx*-1, dy*-1
        antinode1_x, antinode1_y = ax1+idx, ay1+idy
        while 0 <= antinode1_x < width and 0 <= antinode1_y < height:
            antinode_map[antinode1_y][antinode1_x] = "#"
            antinode1_x += idx
            antinode1_y += idy

        ax2, ay2 = antenna_pair["a2"]
        dx, dy = antenna_pair["distance"]
        idx, idy = dx, dy
        antinode2_x, antinode2_y = ax2 + idx, ay2 + idy
        while 0 <= antinode2_x < width and 0 <= antinode2_y < height:
            antinode_map[antinode2_y][antinode2_x] = "#"
            antinode2_x += idx
            antinode2_y += idy

    for antenna_id in antenna_pairs:
        antenna_pair = antenna_pairs[antenna_id]
        ax1, ay1 = antenna_pair["a1"]
        ax2, ay2 = antenna_pair["a2"]
        if 0 <= ax1 < width and 0 <= ay1 < height:
            antinode_map[ay1][ax1] = "#"
        if 0 <= ax2 < width and 0 <= ay2 < height:
            antinode_map[ay1][ax1] = "#"


    antinode_count = 0
    for line in antinode_map:
        for c in line:
            print(c, end="")
            if c == "#": antinode_count += 1
        print()
    print(f'antinodes: {antinode_count}')

if __name__ == "__main__":
    main()