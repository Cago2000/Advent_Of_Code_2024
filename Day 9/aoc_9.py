import string
from copy import deepcopy

def main():
    path = 'disk_map_example.txt'
    disk_map_file = open(path, 'r')
    disk_map = []

    for line in disk_map_file:
        for digit in line:
            if digit != "\n":
                disk_map.append(int(digit))
    print("".join(map(str, disk_map)))
    expanded_disk_map = expand_disk_map(disk_map)
    print("".join(expanded_disk_map))

    expanded_disk_map_single_cell = deepcopy(expanded_disk_map)
    expanded_disk_map_single_cell = defragment_expanded_disk_map_single_cell(expanded_disk_map_single_cell)
    total_sum_single_cell = calculate_checksum(expanded_disk_map_single_cell)
    print(f'total_sum_single_cell: {total_sum_single_cell}')

    files, gaps = get_files_and_gaps(expanded_disk_map)
    expanded_disk_map = defragment_expanded_disk_map(expanded_disk_map, files, gaps)
    total_sum = calculate_checksum(expanded_disk_map)
    print(f'total_sum: {total_sum}')


def defragment_expanded_disk_map_single_cell(expanded_disk_map: list[str]):
    for i, left_c in enumerate(expanded_disk_map):
        if left_c != ".":
            continue
        for j, right_c in enumerate(reversed(expanded_disk_map)):
            j = len(expanded_disk_map)-1-j
            if right_c == ".":
                continue
            expanded_disk_map[i], expanded_disk_map[j] = expanded_disk_map[j], expanded_disk_map[i]
            if is_defragmented(expanded_disk_map):
                return expanded_disk_map
            break
    return expanded_disk_map

def is_defragmented(expanded_disk_map: list[string]) -> bool:
    digit_count = 0
    for c in expanded_disk_map:
        if c != ".":
            digit_count += 1
    digits_in_row = 0
    for c in expanded_disk_map:
        if c == ".": break
        digits_in_row += 1
    if digit_count == digits_in_row:
        return True
    else:
        return False


def defragment_expanded_disk_map(expanded_disk_map: list[str], files: dict[str, dict[str, int | str | int]], gaps: dict[str, dict[str, int | str | int]]):
    restart = True
    while restart:
        for file_id in reversed(files):
            file = files[file_id]
            file_size = file["size"]
            file_start = file["start_index"]
            for gap_id in gaps:
                gap = gaps[gap_id]
                gap_size = gap["size"]
                gap_start = gap["start_index"]
                if file_size > gap_size or file_start < gap_start:
                    continue
                expanded_disk_map = swap_items_on_expanded_disk_map(expanded_disk_map, file, gap)
                files, gaps = get_files_and_gaps(expanded_disk_map)
                break
            restart = False
            if restart:
                break
    return expanded_disk_map

def swap_items_on_expanded_disk_map(expanded_disk_map: list[str], file: dict[str, int | str | int], gap: dict[str, int | str | int]) -> list[str]:
    new_disk_map = expanded_disk_map
    file_start, file_end, file_size = file["start_index"], file["end_index"], file["size"]
    gap_start, gap_end, gap_size = gap["start_index"], gap["end_index"], gap["size"]
    new_disk_map[gap_start:gap_start+file_size], new_disk_map[file_start:file_end+1] = new_disk_map[file_start:file_end+1], new_disk_map[gap_start:gap_start+file_size]
    return new_disk_map

def get_files_and_gaps(expanded_disk_map: list[str]):
    gaps = {}
    gap_id = 0
    files = {}
    index = 0
    for _, c in enumerate(expanded_disk_map):
        if index >= len(expanded_disk_map): break
        c = expanded_disk_map[index]
        size_counter = 0
        size_index = index
        while expanded_disk_map[size_index] == c:
            size_counter += 1
            size_index += 1
            if size_index >= len(expanded_disk_map): break
        if c != ".":
            file = {
                "id": expanded_disk_map[index],
                "size": size_counter,
                "start_index": index,
                "end_index": size_index-1
            }
            files[c] = file
        else:
            gap = {
                "id": gap_id,
                "size": size_counter,
                "start_index": index,
                "end_index": size_index-1
            }
            gaps[gap_id] = gap
            gap_id += 1
        index = size_index
    return files, gaps

def expand_disk_map(disk_map: list[int]):
    expanded_disk_map = []
    file_id = 0
    for i, size in enumerate(disk_map):
        if i%2 == 0:
            for _ in range(size):
                expanded_disk_map.append(str(file_id))
            file_id += 1
        if i%2 == 1:
            for _ in range(size):
                expanded_disk_map.append(".")
    return expanded_disk_map

def calculate_checksum(expanded_disk_map: list[str]) -> int:
    checksum = 0
    for i, c in enumerate(expanded_disk_map):
        if c == ".":
            continue
        checksum += i * int(c)
    return checksum

if __name__ == "__main__":
    main()