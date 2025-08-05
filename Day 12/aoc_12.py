from ordered_set import OrderedSet

def main():
    path = 'garden_example.txt'
    garden_file = open(path, 'r')
    garden = []

    for line in garden_file:
        row = []
        for c in line:
            if c != "\n":
                row.append(c)
        garden.append(row)

    for row in garden:
        for height in row:
            print(height, end="")
        print()
    print()

    regions = get_regions(garden)
    groups = group_coordinates(regions)

    for group_id, group in groups.items():
        print(f'{group["region_str"]}, {group["coords"]}')

def get_regions(garden: list[list[str]]):
    regions = {}
    for y, row in enumerate(garden):
        for x, c in enumerate(row):
            if c not in regions:
                region = {
                    "coords": []
                }
                regions[c] = region
            regions[c]["coords"].append((x, y))
    return regions

def group_coordinates(regions: dict[str, dict[int, list[tuple[int, int]]]]):
    groups = {}
    group_id = 0
    for region_str, region in regions.items():
        region_coordinates = region["coords"]
        group = {
            "region_str": region_str,
            "coords": OrderedSet()
        }
        for region_coord in region_coordinates:
            region_x, region_y = region_coord
            for coord in region_coordinates:
                coord_x, coord_y = coord
                if abs(region_x-coord_x) > 1 or abs(region_y-coord_y) > 1:
                    continue
                group["coords"].add(region_coord)
        groups[group_id] = group
        group_id += 1
    return groups



if __name__ == "__main__":
    main()