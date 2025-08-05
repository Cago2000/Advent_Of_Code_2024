def main():
    path = 'topographic_map.txt'
    topo_map_file = open(path, 'r')
    topo_map = []

    for line in topo_map_file:
        row = []
        for elevation in line:
            if elevation != "\n":
                row.append(int(elevation))
        topo_map.append(row)

    for row in topo_map:
        for height in row:
            print(height, end="")
        print()
    print()

    trailheads = find_trailheads(topo_map)

    scoring_positions = find_scoring_positions(topo_map, trailheads)
    counter = 0
    for trailhead_scoring_positions in scoring_positions:
        counter += len(trailhead_scoring_positions)
    print(f'score: {counter}')

    rating_sum = trace_hiking_paths_init(topo_map, trailheads)
    print(f'rating: {rating_sum}')


def trace_hiking_paths_init(topo_map: list[list[int]], trailheads: dict[tuple[int, int], dict[str, tuple[int, int]]]):
    trailhead_rating_sum = 0
    for trailhead_start, trailhead in trailheads.items():
        trailhead_rating = trace_hiking_paths(topo_map, trailhead_start)
        trailhead_rating_sum += trailhead_rating
    return trailhead_rating_sum

def trace_hiking_paths(topo_map: list[list[int]], path: tuple[int, int]) -> int:
    x, y = path
    if topo_map[y][x] == 9:
        return 1
    total_rating = 0
    valid_paths = find_valid_paths(topo_map, path)
    for valid_path in valid_paths:
        total_rating += trace_hiking_paths(topo_map, valid_path)
    return total_rating

def find_trailheads(topo_map: list[list[int]]):
    trailheads = {}
    for y, line in enumerate(topo_map):
        for x, elevation in enumerate(line):
            if elevation == 0:
                trailhead = {
                    "start": (x, y),
                }
                trailheads[(x, y)] = trailhead
    return trailheads

def find_scoring_positions(topo_map: list[list[int]], trailheads: dict[tuple[int, int], dict[str, tuple[int, int]]]):
    scoring_positions = []
    for trailhead_start, trailhead in trailheads.items():
        trailhead_scoring_positions = set()
        valid_paths = [trailhead_start]
        while len(valid_paths) > 0:
            path = valid_paths.pop(0)
            valid_paths.extend(find_valid_paths(topo_map, path))
            for valid_path in valid_paths:
                x, y = valid_path
                if topo_map[y][x] != 9:
                    continue
                trailhead_scoring_positions.add(valid_path)
        scoring_positions.append(trailhead_scoring_positions)
    return scoring_positions


def find_valid_paths(topo_map: list[list[int]], coords: tuple[int, int]):
    x, y = coords
    width, height = len(topo_map[0]), len(topo_map)
    possible_path_coords = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)]
    valid_paths = []
    for path_coords in possible_path_coords:
        path_x, path_y = path_coords
        if 0 > path_x or path_x >= width or 0 > path_y or path_y >= height:
            continue
        if topo_map[path_y][path_x] - topo_map[y][x] == 1:
            valid_paths.append((path_x, path_y))
    return valid_paths

if __name__ == "__main__":
    main()