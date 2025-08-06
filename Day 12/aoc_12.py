import more_itertools

def main():
    garden = load_file('garden_example.txt')
    all_visited = set()
    regions = []

    for y, row in enumerate(garden):

        for x, c in enumerate(row):
            if (x, y) in all_visited:
                continue
            region, visited = extract_region(garden, (x, y))
            regions.append(region)

            all_visited |= visited


    total_price_task1 = 0
    total_price_task2 = 0
    for i, region in enumerate(regions):
        sides = [[], [], [], []]
        region_coords = region["coords"]
        area = len(region_coords)
        perimeter = 0
        width, height = len(garden[0]), len(garden)
        for region_coord in region_coords:
            region_x, region_y = region_coord
            neighbours = [
                (region_x - 1, region_y), #left
                (region_x + 1, region_y), #right
                (region_x, region_y - 1), #up
                (region_x, region_y + 1)] #down
            for j, neighbour in enumerate(neighbours):
                neighbour_x, neighbour_y = neighbour
                if 0 > neighbour_x or neighbour_x >= width or 0 > neighbour_y or neighbour_y >= height:
                    perimeter += 1
                    sides[j].append((region_x, region_y))
                    continue
                if garden[region_y][region_x] != garden[neighbour_y][neighbour_x]:
                    sides[j].append((region_x, region_y))
                    perimeter += 1
        total_price_task1 += area*perimeter

        changes_per_side = [1, 1, 1, 1]
        for k, side in enumerate(sides):
            match k:
                case 0:
                    sides[k].sort(key=lambda x: (-x[1], x[0]), reverse=True)
                    for a, b in more_itertools.pairwise(sides[k]):
                        ax, ay = a
                        bx, by = b
                        if ax != bx:
                            changes_per_side[k] += 1
                case 1:
                    sides[k].sort(key=lambda x: (-x[1], x[0]), reverse=True)
                    for a, b in more_itertools.pairwise(sides[k]):
                        ax, ay = a
                        bx, by = b
                        if ax != bx:
                            changes_per_side[k] += 1
                case 2:
                    sides[k].sort(key=lambda x: (-x[0], x[1]), reverse=True)
                    for a, b in more_itertools.pairwise(sides[k]):
                        ax, ay = a
                        bx, by = b
                        if ay != by:
                            changes_per_side[k] += 1
                case 3:
                    sides[k].sort(key=lambda x: (-x[0], x[1]), reverse=True)
                    for a, b in more_itertools.pairwise(sides[k]):
                        ax, ay = a
                        bx, by = b
                        if ay != by:
                            changes_per_side[k] += 1

            print(f'{k}: {sides[k]}')
        print(changes_per_side)
        total_price_task2 += sum(changes_per_side)*area
        print(f'Area: {area}, Sides in region: {sum(changes_per_side)}, Region {i}: {region}')
    print(total_price_task1)
    print(total_price_task2)


def extract_region(garden: list[list[str]], start: tuple[int, int]):
    x, y = start
    region = {
        "key_str": garden[y][x],
        "coords": []
    }
    visited = set()
    valid_coords = [start]
    while len(valid_coords) > 0:
        coord = valid_coords.pop(0)
        coord_x, coord_y = coord
        if garden[coord_y][coord_x] == garden[y][x]:
            region["coords"].append(coord)
        visited.add(coord)
        valid_coords.extend(find_valid_coords(garden, coord, visited))
    return region, visited


def find_valid_coords(garden: list[list[str]], coord: tuple[int, int], visited: set):
    x, y = coord
    width, height = len(garden[0]), len(garden)
    possible_path_coords = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)]
    valid_coords = []
    for path_coords in possible_path_coords:
        if path_coords in visited:
            continue
        path_x, path_y = path_coords
        if 0 > path_x or path_x >= width or 0 > path_y or path_y >= height:
            continue
        if garden[path_y][path_x] == garden[y][x]:
            valid_coords.append((path_x, path_y))
            visited.add((path_x, path_y))
    return valid_coords

def load_file(path: str):

    garden_file = open(path, 'r')
    garden = []
    for line in garden_file:
        row = []
        for c in line:
            if c != "\n":
                row.append(c)
        garden.append(row)
    return garden


if __name__ == "__main__":
    main()