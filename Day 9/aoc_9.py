import string

def main():
    path = 'disk_map.txt'
    disk_map_file = open(path, 'r')
    disk_map = []

    for line in disk_map_file:
        for digit in line:
            if digit != "\n":
                disk_map.append(int(digit))

    expanded_disk_map = expand_disk_map(disk_map)
    expanded_disk_map = defragmentate_disk_map(expanded_disk_map)
    checksum = calculate_checksum(expanded_disk_map)
    print(checksum)

def calculate_checksum(expanded_disk_map: list[str]) -> int:
    checksum = 0
    for i, c in enumerate(expanded_disk_map):
        if c == ".":
            continue
        checksum += i * int(c)
    return checksum

def defragmentate_disk_map(expanded_disk_map: list[string]) -> list[string]:
    for a, right_c in enumerate(reversed(expanded_disk_map)):
        i = len(expanded_disk_map)-1-a
        if right_c != ".":
            for j, left_c in enumerate(expanded_disk_map):
                if left_c == ".":
                    expanded_disk_map[j], expanded_disk_map[i] = expanded_disk_map[i], expanded_disk_map[j]
                    if is_defragmentated(expanded_disk_map):
                        return expanded_disk_map
                    break
    return expanded_disk_map


def expand_disk_map(disk_map: list[int]) -> list[str]:
    expanded_disk_map = []
    file_id = 0
    for i, size in enumerate(disk_map):
            for _ in range(size):
                if i % 2 == 0:
                    expanded_disk_map.append(str(file_id))
                if i%2 == 1:
                    expanded_disk_map.append(".")
            if i%2 == 0:
                file_id += 1
    return expanded_disk_map

def reduce_disk_map(expanded_disk_map : list[str]) -> list[int]:
    disk_map = []
    key = expanded_disk_map[0]
    counter = 0
    for i, c in enumerate(expanded_disk_map):
        if c == key:
            counter += 1
        else:
            disk_map.append(counter)
            key = c
            counter = 1
        if i == len(expanded_disk_map)-1:
            disk_map.append(counter)
    return disk_map

def is_defragmentated(expanded_disk_map: list[string]) -> bool:
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

if __name__ == "__main__":
    main()